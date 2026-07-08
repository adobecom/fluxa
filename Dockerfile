# Fluxa ActionJSON backend — FastAPI + DeepAgents + Adobe Photoshop API
# deepagents requires Python >= 3.11
FROM python:3.11-slim

# Keep Python output unbuffered so logs stream to `fly logs`.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install Python dependencies first (better layer caching).
# No system packages needed: yt-dlp downloads audio-only streams directly,
# so ffmpeg is not required.
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the application code (secrets come from `fly secrets`, NOT the image).
COPY . .

# Must match [http_service].internal_port in fly.toml.
EXPOSE 8000

# server.py starts uvicorn on 0.0.0.0:8000
CMD ["python", "server.py"]
