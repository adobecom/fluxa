"""
Fluxa ActionJSON Server - Deep Agent Version

This server exposes the Fluxa functionality as an API using the deep agent
(AgentPhotoshopActionGenerator) for ActionJSON generation.

Requirements:
    - Python 3.11+ (deepagents requires Python >= 3.11)
    - Run with: python3.11 server.py

Endpoints:
    POST /apply - Process images with a YouTube tutorial
    GET /download/{job_id} - Download processed files
    GET /health - Health check
"""

from __future__ import annotations

import base64
import json
import logging
import mimetypes
import os
import re
import sys
import uuid
from pathlib import Path
from typing import List, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

# Setup paths
REPO_ROOT = Path(__file__).resolve().parent
RUNS_DIR = REPO_ROOT / "runs"
RUNS_DIR.mkdir(parents=True, exist_ok=True)
DOCS_PATH = REPO_ROOT / "ps_action_docs"

# Add repo root to path so the local `fluxa` package is importable
sys.path.insert(0, str(REPO_ROOT))

# Load environment variables from root .env
load_dotenv(REPO_ROOT / ".env")

# Now import fluxa components
from fluxa.extractors.youtube_extractor import YouTubeExtractor
from fluxa.generators.agent_photoshop_action_generator import AgentPhotoshopActionGenerator

# Import actions processor
from actions import process_with_actionjson

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
LOGGER = logging.getLogger("fluxa.server")

# Configuration
MODEL = "gpt-5.1"
TIMEOUT = 180  # Increased timeout for agent operations (3 minutes)
MAX_TRANSCRIPT_LENGTH = 50000

# Debug flag: When True, always use transcript from transcript.txt instead of YouTube
USE_LOCAL_TRANSCRIPT = False
LOCAL_TRANSCRIPT_PATH = REPO_ROOT / "transcript.txt"

# Debug flag: When True, skip agent generation and use hardcoded pencil.json
USE_HARDCODED_PENCIL_JSON = False
HARDCODED_JSON_PATH = REPO_ROOT / "json_examples" / "pencil.json"

# Download registry for serving files
DOWNLOAD_REGISTRY: dict[str, Path] = {}

# FastAPI app
app = FastAPI(
    title="Fluxa ActionJSON Server (Deep Agent)",
    version="0.2.0",
    description=(
        "Backend for generating Photoshop ActionJSON payloads using DeepAgents and "
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


# =============================================================================
# Pydantic Models (same as ref.py for compatibility)
# =============================================================================


class GenerateResponse(BaseModel):
    job_id: str
    output_path: str
    actions_only_path: str
    actions_count: int
    actions: Optional[List[dict]] = None


class ApplyResponse(BaseModel):
    job_id: str
    output_path: str
    download_url: Optional[str] = None
    preview_path: Optional[str] = None


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
    openai_configured: bool
    adobe_configured: bool


# =============================================================================
# Helper Functions
# =============================================================================


def _check_environment() -> dict[str, bool]:
    """Check if required environment variables are set."""
    return {
        "openai": bool(os.getenv("OPENAI_API_KEY")),
        "adobe": bool(os.getenv("CLIENT_ID") and os.getenv("CLIENT_SECRET")),
        "r2": bool(
            os.getenv("R2_ACCOUNT_ID")
            and os.getenv("R2_BUCKET_NAME")
            and os.getenv("R2_ACCESS_KEY_ID")
            and os.getenv("R2_SECRET_ACCESS_KEY")
        ),
    }


def _prepare_run_directory(job_id: str) -> Path:
    """Create a run directory for this job."""
    run_dir = RUNS_DIR / job_id
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


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


def _extract_youtube_transcript(url: str) -> dict:
    """Extract transcript from YouTube video.

    Uses captions when available, and falls back to Whisper audio
    transcription (via the OpenAI key) when captions are disabled/missing.
    """
    LOGGER.info(f"Extracting transcript from: {url}")
    extractor = YouTubeExtractor()
    result = extractor.extract(
        url,
        max_length=MAX_TRANSCRIPT_LENGTH,
        whisper_api_key=os.getenv("OPENAI_API_KEY"),
    )
    LOGGER.info(
        f"Transcript extracted via '{result.get('type')}': "
        f"{len(result['content'])} characters"
    )
    return result


def _generate_actions_with_agent(
    content: str,
    source: str,
    source_type: str,
) -> dict:
    """Generate ActionJSON using the deep agent."""
    LOGGER.info("Initializing AgentPhotoshopActionGenerator...")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set in environment")
    
    generator = AgentPhotoshopActionGenerator(
        api_key=api_key,
        model=MODEL,
        docs_path=str(DOCS_PATH),
        timeout=TIMEOUT,
    )
    
    LOGGER.info("Generating actions with deep agent...")
    result = generator.generate(
        content=content,
        source=source,
        source_type=source_type,
    )
    
    LOGGER.info(f"Generated {len(result['actions'])} actions")
    return result


def _save_actions_to_file(actions: List[dict], run_dir: Path) -> tuple[Path, Path]:
    """Save actions to JSON files."""
    # Full output with metadata
    output_path = run_dir / "output.json"
    actions_only_path = run_dir / "actions.json"
    
    # Save full output
    full_output = {
        "actions": actions,
        "generator": "deep_agent",
        "model": MODEL,
    }
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(full_output, f, indent=2)
    
    # Save actions only (for Photoshop API)
    with actions_only_path.open("w", encoding="utf-8") as f:
        json.dump(actions, f, indent=2)
    
    return output_path, actions_only_path


def _build_inline_render_payload(file_path: str) -> InlineRenderPayload:
    """Build base64 encoded payload for inline render response."""
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


def _run_pipeline(
    tutorial_url: str,
    image_paths: List[str],
    inline_render: bool = False,
) -> PipelineResponse:
    """
    Run the full pipeline:
    1. Extract transcript from YouTube
    2. Generate ActionJSON with deep agent
    3. Apply actions via Adobe Photoshop API
    """
    job_id = uuid.uuid4().hex
    run_dir = _prepare_run_directory(job_id)
    
    LOGGER.info(f"Starting pipeline job: {job_id}")
    LOGGER.info(f"Tutorial URL: {tutorial_url}")
    LOGGER.info(f"Image paths: {image_paths}")
    
    # Step 1: Extract transcript (or use local file if flag is set)
    if USE_LOCAL_TRANSCRIPT and LOCAL_TRANSCRIPT_PATH.exists():
        LOGGER.info(f"Step 1: Using local transcript from {LOCAL_TRANSCRIPT_PATH}")
        with open(LOCAL_TRANSCRIPT_PATH, 'r', encoding='utf-8') as f:
            transcript_content = f.read()
        extracted = {
            "content": transcript_content,
            "source": str(LOCAL_TRANSCRIPT_PATH),
            "type": "local_transcript"
        }
        LOGGER.info(f"Local transcript loaded: {len(transcript_content)} characters")
    else:
        LOGGER.info("Step 1: Extracting YouTube transcript...")
        extracted = _extract_youtube_transcript(str(tutorial_url))
    
    # Step 2: Generate actions (or use hardcoded JSON if flag is set)
    if USE_HARDCODED_PENCIL_JSON and HARDCODED_JSON_PATH.exists():
        LOGGER.info(f"Step 2: Using hardcoded JSON from {HARDCODED_JSON_PATH}")
        with open(HARDCODED_JSON_PATH, 'r', encoding='utf-8') as f:
            # Read and parse JSON (pencil.json has comments, so we need to strip them)
            content = f.read()
            # Remove single-line comments (// ...)
            content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            actions = json.loads(content)
        LOGGER.info(f"Hardcoded JSON loaded: {len(actions)} actions")
    else:
        LOGGER.info("Step 2: Generating ActionJSON with deep agent...")
        generation_result = _generate_actions_with_agent(
            content=extracted["content"],
            source=extracted["source"],
            source_type=extracted["type"],
        )
        actions = generation_result["actions"]

    # Guard: if no actions were produced, the transcript had no usable Photoshop
    # steps (e.g. a music-only video). Fail clearly instead of sending an empty
    # array to Adobe, which returns a confusing 400.
    if not actions:
        raise ValueError(
            "Couldn't extract any Photoshop steps from this tutorial. The video "
            "may have no spoken/caption instructions (e.g. music-only). Try a "
            "narrated or captioned Photoshop tutorial."
        )

    # Save actions to files
    output_path, actions_only_path = _save_actions_to_file(actions, run_dir)
    
    generation_response = GenerateResponse(
        job_id=job_id,
        output_path=str(output_path),
        actions_only_path=str(actions_only_path),
        actions_count=len(actions),
    )
    
    # Step 3: Apply actions via Adobe Photoshop API
    LOGGER.info("Step 3: Applying actions via Adobe Photoshop API...")
    render_output_path = str(run_dir / "output.psd")
    
    result = process_with_actionjson(
        input_images=image_paths,
        action_json_file=str(actions_only_path),
        output_path=render_output_path,
    )
    
    if not result:
        raise RuntimeError("Photoshop API job failed; see server logs for details.")
    
    # Handle both dict and string return types
    if isinstance(result, dict):
        final_output_path = result.get("output_path", render_output_path)
        preview_path = result.get("preview_path")
    else:
        final_output_path = result
        preview_path = None
    
    # Register for download
    DOWNLOAD_REGISTRY[job_id] = Path(final_output_path).resolve()
    
    application_response = ApplyResponse(
        job_id=job_id,
        output_path=str(final_output_path),
        download_url=f"/download/{job_id}",
        preview_path=preview_path,
    )
    
    # Build inline render if requested - use preview_path (PNG) for browser display
    inline_payload = None
    if inline_render:
        # Prefer preview_path (PNG) as browsers can display it
        target_path = preview_path or final_output_path
        if target_path:
            inline_payload = _build_inline_render_payload(target_path)
    
    LOGGER.info(f"Pipeline completed successfully: {job_id}")
    
    return PipelineResponse(
        pipeline_id=job_id,
        generation=generation_response,
        application=application_response,
        inline_render=inline_payload,
    )


# =============================================================================
# API Endpoints
# =============================================================================


@app.get("/health", response_model=HealthResponse, tags=["system"])
async def health() -> HealthResponse:
    """Health check endpoint."""
    env_status = _check_environment()
    all_ready = all(env_status.values())
    
    return HealthResponse(
        status="ok" if all_ready else "setup-required",
        generator_ready=DOCS_PATH.exists(),
        openai_configured=env_status["openai"],
        adobe_configured=env_status["adobe"] and env_status["r2"],
    )


@app.post("/apply", response_model=PipelineResponse, tags=["actions"])
async def apply_endpoint(
    tutorial_url: str = Form(..., description="YouTube tutorial URL"),
    inline_render: bool = Form(False, description="Include base64 encoded result in response"),
    images: List[UploadFile] = File(..., description="Input image files"),
) -> PipelineResponse:
    """
    Process images using a YouTube Photoshop tutorial.
    
    This endpoint:
    1. Extracts the transcript from the YouTube video
    2. Uses a deep agent to generate Photoshop ActionJSON
    3. Executes the actions via Adobe Photoshop API
    4. Returns the processed image (PNG preview for browser display)
    
    Args:
        tutorial_url: YouTube video URL containing Photoshop tutorial
        inline_render: If true, include base64 encoded PNG preview in response
        images: One or more input images to process
    
    Returns:
        PipelineResponse with job details and download URL
    """
    if not images:
        raise HTTPException(status_code=400, detail="At least one image file is required.")
    
    # Check environment
    env_status = _check_environment()
    if not env_status["openai"]:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not configured")
    if not env_status["adobe"] or not env_status["r2"]:
        raise HTTPException(status_code=500, detail="Adobe/R2 credentials not configured")
    
    upload_job_id = uuid.uuid4().hex
    
    try:
        # Save uploaded images
        image_paths = await _save_uploaded_images(upload_job_id, images)
        
        # Run the pipeline in a thread pool (blocking operations)
        return await run_in_threadpool(
            _run_pipeline,
            tutorial_url,
            image_paths,
            inline_render,
        )
    except HTTPException:
        raise
    except ValueError as exc:
        # Validation errors (e.g., invalid YouTube URL, no transcript)
        LOGGER.exception("Validation error in pipeline")
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        LOGGER.exception("Pipeline failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/download/{job_id}", tags=["actions"])
async def download_endpoint(job_id: str) -> FileResponse:
    """
    Download a processed file by job ID.
    
    Args:
        job_id: The job ID returned from /apply endpoint
    
    Returns:
        The processed file (PSD format)
    """
    path = DOWNLOAD_REGISTRY.get(job_id)
    if not path or not path.exists():
        raise HTTPException(status_code=404, detail="File not found for the given job_id")
    
    return FileResponse(
        path,
        media_type="application/octet-stream",
        filename=path.name,
    )


# =============================================================================
# Main Entry Point
# =============================================================================


if __name__ == "__main__":
    import uvicorn
    
    # Check Python version
    if sys.version_info < (3, 11):
        print("ERROR: This server requires Python 3.11 or higher.")
        print(f"Current version: {sys.version}")
        print("Run with: python3.11 server.py")
        sys.exit(1)
    
    LOGGER.info("Starting Fluxa ActionJSON Server (Deep Agent)...")
    LOGGER.info(f"Python version: {sys.version}")
    LOGGER.info(f"Repository root: {REPO_ROOT}")
    LOGGER.info(f"Docs path: {DOCS_PATH}")
    LOGGER.info(f"Runs directory: {RUNS_DIR}")
    
    # Check environment on startup
    env_status = _check_environment()
    LOGGER.info(f"Environment status: {env_status}")
    
    if not all(env_status.values()):
        LOGGER.warning("Some environment variables are not configured!")
        LOGGER.warning("Required: OPENAI_API_KEY, CLIENT_ID, CLIENT_SECRET, R2_* credentials")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)

