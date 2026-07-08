# Fluxa

Turn a Photoshop tutorial (YouTube video) into an edited image. Fluxa extracts the
tutorial transcript, uses a deep agent to generate Photoshop **ActionJSON**, and
executes it against the Adobe Photoshop API — returning a rendered PSD and a PNG preview.

## Pipeline

1. **Extract** – pull the transcript from a YouTube URL (`fluxa/extractors`).
2. **Generate** – a deep agent reads `ps_action_docs/` and converts the transcript
   into Photoshop ActionJSON (`fluxa/generators/agent_photoshop_action_generator.py`).
3. **Apply** – upload input images to Cloudflare R2, call Adobe's `actionJSON` API,
   download the resulting PSD + PNG preview (`actions.py`).

## Project structure

```
fluxa-re/
├── server.py            # FastAPI server exposing /apply, /download, /health
├── actions.py           # Adobe Photoshop API executor + Cloudflare R2 storage
├── fluxa/               # Generator package
│   ├── extractors/      # YouTube / web transcript extractors
│   ├── generators/      # Deep-agent ActionJSON generator
│   ├── knowledge/       # Photoshop operation knowledge base
│   ├── prompts/         # Prompt templates
│   └── utils/           # Formatting / validation helpers
├── ps_action_docs/      # Atomic + composite action docs the agent reads at runtime
├── frontend/            # Static demo UI (index.html, script.js, styles.css)
├── requirements.txt
└── .env                 # Secrets & config (not committed)
```

## Setup

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` with:

```
OPENAI_API_KEY=sk-...
CLIENT_ID=...            # Adobe API client id
CLIENT_SECRET=...        # Adobe API client secret
R2_ACCOUNT_ID=...        # Cloudflare R2
R2_BUCKET_NAME=...
R2_ACCESS_KEY_ID=...
R2_SECRET_ACCESS_KEY=...
R2_REGION=auto
```

## Run

Start the backend (requires Python 3.11+ and outbound internet for YouTube/OpenAI/Adobe):

```bash
python3.11 server.py          # serves on http://0.0.0.0:8000
```

Serve the frontend (separate terminal):

```bash
python3.11 -m http.server 5500 --directory frontend
# open http://localhost:5500
```

## API

- `POST /apply` – form fields: `tutorial_url`, `inline_render` (bool), `images[]`.
- `GET  /download/{job_id}` – download the rendered PSD.
- `GET  /health` – readiness + which credentials are configured.

## Notes

- The tutorial video **must have English captions/spoken instructions**; music-only
  videos produce no usable transcript.
- Adobe input images must be `.psd/.jpg/.jpeg/.tif/.png` (no `.webp`/`.avif`).
- Interactive tutorial steps (freehand mask painting, eyedropper color-picking) have
  no deterministic ActionJSON equivalent and may not render exactly.
