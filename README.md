# Photoshop API Executor

A general-purpose tool to execute Photoshop actions defined in JSON files on images using the Adobe Photoshop API.

## Fluxa + Photoshop workflow helper

Use `run.sh` to manage the end-to-end pipeline without repeatedly re-installing dependencies:

1. `./run.sh setup` – installs the Fluxa generator (inside `actionJSON-generator/venv`) and adds the executor dependencies (`requests`, `boto3`, etc.) to the same environment. Run this once or whenever you need to refresh dependencies.
2. `./run.sh generate <tutorial_url> [--output path] [--actions-only path]` – creates a full Fluxa JSON from a tutorial and writes the executable `actions` array to a separate file.
3. `./run.sh apply <image_paths> <actions_file> [--output path]` – uploads the provided images, calls the Adobe ActionJSON API, and downloads the rendered PSD/JPG.
4. `./run.sh pipeline <tutorial_url> <image_paths> [...]` – convenient wrapper that runs generate + apply in a single command, mirroring the old `run.sh` behavior.

The script expects `jq` to be available on your system and will prompt you to run `setup` if the virtual environment has not been created yet. This separation makes it easier to call the generation and execution steps independently from a backend/API surface.

## API Server

Expose the workflow to a frontend by running the FastAPI server in `server/main.py`.

1. Run `./run.sh setup` once to create `actionJSON-generator/venv` and install FastAPI/uvicorn.
2. Start the server: `./run.sh serve --host 0.0.0.0 --port 8000 --reload`
3. Available endpoints:
   - `GET /health` – readiness probe (checks that the shared venv exists)
   - `POST /apply` – `multipart/form-data` request that accepts `tutorial_url`, optional `inline_render`, and one or more image files (field name `images`). Uploaded files are stored server-side and fed into the pipeline automatically.

> **CORS**: When serving the frontend from a different origin (e.g., `npm run dev`), set the `FLUXA_CORS_ALLOW_ORIGINS` environment variable with a comma-separated list of allowed origins (for example `http://localhost:5173,http://localhost:4173`). If unset, the API defaults to `*`.


Every request creates a unique run directory under `actionJSON-generator/runs/<job_id>` unless you provide explicit output paths. Responses include file paths plus, for apply/pipeline, `application.download_url` (served by `/download/{job_id}`), a `preview_path` (PNG used for inline previews), and an optional inline base64 payload when requested.

### Example: frontend fetch for `POST /pipeline`

```javascript
async function runPipeline() {
  const response = await fetch("https://your-fluxa-host/apply", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      tutorial_url: "https://www.youtube.com/watch?v=VIDEO_ID",
      image_paths: ["input_images/airbaloon.jpg"],
      inline_render: true
    })
  });

  if (!response.ok) {
    throw new Error(`Pipeline failed: ${response.status}`);
  }

  const payload = await response.json();
  const { inline_render } = payload;
  if (inline_render) {
    const blob = await (await fetch(`data:${inline_render.content_type};base64,${inline_render.base64_data}`)).blob();
    const url = URL.createObjectURL(blob);
    // e.g., attach to a download link:
    const link = document.createElement("a");
    link.href = url;
    link.download = inline_render.filename;
    link.click();
    URL.revokeObjectURL(url);
  } else {
    console.log("Download via:", payload.application.download_url);
  }
}
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root:
```bash
cp .env.example .env
```

3. Add your API credentials to `.env`:
   - `CLIENT_ID`: Your Adobe Client ID
   - `CLIENT_SECRET`: Your Adobe Client Secret
   - `DROPBOX_ACCESS_TOKEN`: Your Dropbox Access Token

## Usage

### Basic usage:
```bash
python photoshop-actions.py input_images/image.jpg action.json
```

### Specify output path:
```bash
python photoshop-actions.py input_images/image.jpg action.json output_images/result.jpg
```

## Directory Structure

```
.
├── aeroplane_remove.py    # Main script
├── input_images/          # Place your input images here
├── output_images/         # Processed images will be saved here
├── .env                   # Your API credentials (create this)
├── .env.example           # Example environment file
└── requirements.txt       # Python dependencies
```

## Action JSON Format

Create a JSON file with an array of Photoshop action objects. See `action_example.json` for a reference.

Example `action.json`:
```json
[
    {
        "_obj": "set",
        "_target": [{ "_property": "selection", "_ref": "channel" }],
        "to": {
            "_obj": "rectangle",
            "left": { "_unit": "pixelsUnit", "_value": 100.0 },
            "top": { "_unit": "pixelsUnit", "_value": 100.0 },
            "right": { "_unit": "pixelsUnit", "_value": 300.0 },
            "bottom": { "_unit": "pixelsUnit", "_value": 300.0 }
        }
    },
    {
        "_obj": "fill",
        "mode": { "_enum": "blendMode", "_value": "normal" },
        "opacity": { "_unit": "percentUnit", "_value": 100.0 },
        "using": { "_enum": "fillContents", "_value": "contentAware" }
    }
]
```

## Notes

- The script uses Dropbox as intermediate storage for the Adobe Photoshop API
- Action JSON files can include comments (single-line `//` or multi-line `/* */`) which will be automatically removed
- Output images are automatically saved to `output_images/` directory if no output path is specified
