from __future__ import annotations

import json
import logging
import os
import subprocess
import sys
import uuid
from pathlib import Path
from typing import List, Optional

import base64
import mimetypes

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, HttpUrl, validator

from actions import process_with_actionjson

LOGGER = logging.getLogger("fluxa.api")

REPO_ROOT = Path(__file__).resolve().parent.parent
GENERATOR_DIR = REPO_ROOT / "actionJSON-generator"
RUNS_DIR = GENERATOR_DIR / "runs"
RUNS_DIR.mkdir(parents=True, exist_ok=True)
FRONTEND_DIR = REPO_ROOT / "frontend"
DOWNLOAD_REGISTRY: dict[str, Path] = {}

app = FastAPI(
    title="Fluxa ActionJSON Server",
    version="0.1.0",
    description=(
        "Backend helper for generating Photoshop ActionJSON payloads with Fluxa and "
        "executing them via the Adobe Photoshop API."
    ),
)


def _parse_cors_origins(value: Optional[str]) -> list[str]:
    """Split FLUXA_CORS_ALLOW_ORIGINS env var into a cleaned list."""
    if not value:
        return ["*"]
    origins = [item.strip() for item in value.split(",")]
    return [origin for origin in origins if origin]


ALLOWED_ORIGINS = _parse_cors_origins(os.environ.get("FLUXA_CORS_ALLOW_ORIGINS"))
ALLOW_CREDENTIALS = "*" not in ALLOWED_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=ALLOW_CREDENTIALS,
    allow_methods=["*"],
    allow_headers=["*"],
)

if FRONTEND_DIR.exists():
    app.mount("/app", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")


def _assert_generator_setup() -> None:
    """Ensure the shared Fluxa virtual environment exists."""
    if not (GENERATOR_DIR / "venv").exists():
        raise RuntimeError(
            f"Fluxa virtual environment not found at {GENERATOR_DIR / 'venv'}; "
            "run './run.sh setup' before starting the API server."
        )


def _prepare_output_paths(
    output_path: Optional[str],
    actions_only_path: Optional[str],
) -> tuple[str, Path, Path]:
    """Create per-request directories and resolve final file paths."""
    job_id = uuid.uuid4().hex
    run_dir = RUNS_DIR / job_id
    run_dir.mkdir(parents=True, exist_ok=True)

    def _resolve(path_str: Optional[str], default_name: str) -> Path:
        if path_str:
            path = Path(path_str).expanduser()
        else:
            path = run_dir / default_name
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    json_path = _resolve(output_path, "output.json")
    actions_path = _resolve(actions_only_path, "actions.json")
    return job_id, json_path, actions_path


async def _save_uploaded_images(job_id: str, uploads: List[UploadFile]) -> List[str]:
    """Persist uploaded files to disk and return their paths."""
    upload_dir = RUNS_DIR / job_id / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)
    saved_paths: List[str] = []

    for idx, upload in enumerate(uploads):
        filename = Path(upload.filename or f"image_{idx}.bin").name
        destination = upload_dir / filename
        data = await upload.read()
        with destination.open("wb") as f:
            f.write(data)
        await upload.close()
        saved_paths.append(str(destination))

    return saved_paths


def _run_fluxa_cli(tutorial_url: str, output_path: Path) -> None:
    """Invoke the Fluxa CLI to produce the full action JSON."""
    tutorial_arg = str(tutorial_url)
    cmd = [sys.executable, "-m", "fluxa.cli", tutorial_arg, "-o", str(output_path)]
    LOGGER.info("Running Fluxa CLI: %s", " ".join(cmd))
    result = subprocess.run(
        cmd,
        cwd=str(GENERATOR_DIR),
        capture_output=True,
        text=True,
        env=os.environ.copy(),
    )
    if result.returncode != 0:
        LOGGER.error("Fluxa CLI failed: %s", result.stderr or result.stdout)
        raise RuntimeError(f"Fluxa CLI failed: {result.stderr or result.stdout}")
    LOGGER.info("Fluxa CLI completed: %s", output_path)


def _extract_actions(output_path: Path, actions_path: Path) -> List[dict]:
    """Load the Fluxa output and write the executable actions subset."""
    with output_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict) and "actions" in data:
        actions = data["actions"]
    elif isinstance(data, list):
        actions = data
    else:
        raise ValueError("Fluxa output missing 'actions' array")

    with actions_path.open("w", encoding="utf-8") as f:
        json.dump(actions, f, indent=2)

    return actions


class GenerateRequest(BaseModel):
    tutorial_url: HttpUrl = Field(..., description="Tutorial URL (YouTube or article) for Fluxa.")
    output_path: Optional[str] = Field(
        None,
        description="Destination for the full Fluxa JSON output. Defaults to a temp run folder.",
    )
    actions_only_path: Optional[str] = Field(
        None,
        description="Where to store the extracted actions array (used by the Photoshop API).",
    )
    include_actions: bool = Field(
        False,
        description="Return the generated actions array in the API response.",
    )


class GenerateResponse(BaseModel):
    job_id: str
    output_path: str
    actions_only_path: str
    actions_count: int
    actions: Optional[List[dict]] = None


class ApplyRequest(BaseModel):
    image_paths: List[str] = Field(..., min_items=1, description="List of local image file paths.")
    action_json_path: str = Field(..., description="Path to the actions-only JSON payload.")
    output_path: Optional[str] = Field(
        None,
        description="Optional override for the Photoshop API output path.",
    )

    @validator("image_paths", each_item=True)
    def _validate_image_path(cls, value: str) -> str:
        if not Path(value).exists():
            raise ValueError(f"Image not found: {value}")
        return value

    @validator("action_json_path")
    def _validate_action_path(cls, value: str) -> str:
        if not Path(value).exists():
            raise ValueError(f"Action JSON not found: {value}")
        return value


class ApplyResponse(BaseModel):
    job_id: str
    output_path: str
    download_url: Optional[str] = None
    preview_path: Optional[str] = None


class PipelineRequest(BaseModel):
    tutorial_url: HttpUrl
    image_paths: List[str] = Field(..., min_items=1)
    json_output_path: Optional[str] = None
    actions_only_path: Optional[str] = None
    render_output_path: Optional[str] = None
    include_actions: bool = False
    inline_render: bool = Field(
        False,
        description="If true, include the rendered file bytes (base64) directly in the response.",
    )

    @validator("image_paths", each_item=True)
    def _validate_images(cls, value: str) -> str:
        if not Path(value).exists():
            raise ValueError(f"Image not found: {value}")
        return value


class InlineRenderPayload(BaseModel):
    filename: str
    content_type: str
    base64_data: str


class PipelineResponse(BaseModel):
    pipeline_id: str
    generation: GenerateResponse
    application: ApplyResponse
    inline_render: Optional[InlineRenderPayload] = None


class HealthResponse(BaseModel):
    status: str
    generator_ready: bool


def _generate_actions(request: GenerateRequest) -> GenerateResponse:
    _assert_generator_setup()
    job_id, json_path, actions_path = _prepare_output_paths(
        request.output_path,
        request.actions_only_path,
    )
    _run_fluxa_cli(request.tutorial_url, json_path)
    actions = _extract_actions(json_path, actions_path)

    response = GenerateResponse(
        job_id=job_id,
        output_path=str(json_path),
        actions_only_path=str(actions_path),
        actions_count=len(actions),
    )
    if request.include_actions:
        response.actions = actions
    return response


def _apply_actions(request: ApplyRequest) -> ApplyResponse:
    _assert_generator_setup()
    job_id = uuid.uuid4().hex
    output_path = request.output_path
    result = process_with_actionjson(
        input_images=request.image_paths,
        action_json_file=request.action_json_path,
        output_path=output_path,
    )
    if not result:
        raise RuntimeError("Photoshop API job failed; see server logs for details.")
    if isinstance(result, dict):
        final_output_path = result.get("output_path")
        preview_path = result.get("preview_path")
    else:
        final_output_path = result
        preview_path = None

    DOWNLOAD_REGISTRY[job_id] = Path(final_output_path).resolve()
    return ApplyResponse(
        job_id=job_id,
        output_path=str(final_output_path),
        download_url=f"/download/{job_id}",
        preview_path=preview_path,
    )


def _run_pipeline(request: PipelineRequest) -> PipelineResponse:
    generation_request = GenerateRequest(
        tutorial_url=request.tutorial_url,
        output_path=request.json_output_path,
        actions_only_path=request.actions_only_path,
        include_actions=request.include_actions,
    )
    generation_result = _generate_actions(generation_request)

    application_request = ApplyRequest(
        image_paths=request.image_paths,
        action_json_path=generation_result.actions_only_path,
        output_path=request.render_output_path,
    )
    application_result = _apply_actions(application_request)

    inline_payload = None
    if request.inline_render:
        target_path = application_result.preview_path or application_result.output_path
        if target_path:
            inline_payload = _build_inline_render_payload(target_path)

    return PipelineResponse(
        pipeline_id=generation_result.job_id,
        generation=generation_result,
        application=application_result,
        inline_render=inline_payload,
    )


def _build_inline_render_payload(file_path: str) -> InlineRenderPayload:
    path = Path(file_path)
    if not path.exists():
        raise RuntimeError(f"Rendered file not found at {file_path}")
    mime_type, _ = mimetypes.guess_type(path.name)
    mime_type = mime_type or "application/octet-stream"
    with path.open("rb") as f:
        encoded = base64.b64encode(f.read()).decode("ascii")
    return InlineRenderPayload(
        filename=path.name,
        content_type=mime_type,
        base64_data=encoded,
    )


@app.get("/health", response_model=HealthResponse, tags=["system"])
async def health() -> HealthResponse:
    ready = (GENERATOR_DIR / "venv").exists()
    return HealthResponse(status="ok" if ready else "setup-required", generator_ready=ready)

@app.post("/apply", response_model=PipelineResponse, tags=["actions"])
async def pipeline_upload_endpoint(
    tutorial_url: str = Form(...),
    inline_render: bool = Form(False),
    images: List[UploadFile] = File(...),
) -> PipelineResponse:
    if not images:
        raise HTTPException(status_code=400, detail="At least one image file is required.")

    upload_job_id = uuid.uuid4().hex
    try:
        image_paths = await _save_uploaded_images(upload_job_id, images)
        pipeline_request = PipelineRequest(
            tutorial_url=tutorial_url,
            image_paths=image_paths,
            inline_render=inline_render,
        )
        return await run_in_threadpool(_run_pipeline, pipeline_request)
    except HTTPException:
        raise
    except Exception as exc:
        LOGGER.exception("Pipeline upload endpoint failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/download/{job_id}", tags=["actions"])
async def download_endpoint(job_id: str) -> FileResponse:
    path = DOWNLOAD_REGISTRY.get(job_id)
    if not path or not path.exists():
        raise HTTPException(status_code=404, detail="File not found for the given job_id")
    return FileResponse(
        path,
        media_type="application/octet-stream",
        filename=path.name,
    )

