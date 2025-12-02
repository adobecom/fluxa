#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GENERATOR_DIR="$REPO_ROOT/actionJSON-generator"
GENERATOR_VENV="$GENERATOR_DIR/venv"
DEFAULT_JSON_OUTPUT="$GENERATOR_DIR/output.json"
DEFAULT_ACTIONS_ONLY="$GENERATOR_DIR/temp.json"

GENERATED_ACTIONS_PATH=""

usage() {
  cat <<'EOF'
Fluxa pipeline helper

Usage:
  ./run.sh setup
      Install/refresh dependencies (Fluxa generator + action executor).

  ./run.sh generate <tutorial_url> [--output <file>] [--actions-only <file>]
      Create an action JSON from a tutorial link. Defaults write to
      actionJSON-generator/output.json and actionJSON-generator/temp.json.

  ./run.sh apply <image_paths> <action_json_file> [--output <file>]
      Apply an existing action JSON to one or more images (comma-separated paths).

  ./run.sh pipeline <tutorial_url> <image_paths>
      [--json-output <file>] [--actions-only <file>] [--output <file>]
      Run generation followed by application in a single command.

  ./run.sh serve [--host <host>] [--port <port>] [--reload]
      Start the FastAPI server (uvicorn server.main:app) using the shared venv.

If no explicit command is provided but two positional arguments are passed,
the script falls back to the legacy pipeline mode:
  ./run.sh <tutorial_url> <image_paths>

Examples:
  ./run.sh setup
  ./run.sh generate https://youtu.be/... --output output.json
  ./run.sh apply input_images/img.jpg actionJSON-generator/temp.json --output output_images/result.psd
  ./run.sh pipeline https://youtu.be/... input_images/img.jpg --output output_images/result.psd
EOF
}

ensure_tool() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Error: required tool '$1' not found in PATH." >&2
    exit 1
  fi
}

ensure_generator_env() {
  if [ ! -f "$GENERATOR_VENV/bin/activate" ]; then
    cat <<EOF >&2
Error: Fluxa virtual environment not found at $GENERATOR_VENV
Run './run.sh setup' once before generating or applying actions.
EOF
    exit 1
  fi
}

run_setup() {
  echo "[setup] Preparing Fluxa environments..."
  if [ ! -d "$GENERATOR_VENV" ]; then
    (cd "$GENERATOR_DIR" && ./setup.sh)
  else
    echo "[setup] Reusing generator environment at $GENERATOR_VENV"
  fi

  # Install Photoshop executor dependencies inside the same venv
  # shellcheck disable=SC1090
  source "$GENERATOR_VENV/bin/activate"
  pip install -r "$REPO_ROOT/requirements.txt"
  deactivate || true
  echo "[setup] Complete."
}

run_generate() {
  if [ $# -lt 1 ]; then
    echo "Error: tutorial URL is required for generate command." >&2
    usage
    exit 1
  fi

  local tutorial_url="$1"
  shift
  local output_file="$DEFAULT_JSON_OUTPUT"
  local actions_only="$DEFAULT_ACTIONS_ONLY"

  while [ $# -gt 0 ]; do
    case "$1" in
      --output|-o)
        output_file="$2"
        shift 2
        ;;
      --actions-only|-a)
        actions_only="$2"
        shift 2
        ;;
      *)
        echo "Unknown generate option: $1" >&2
        exit 1
        ;;
    esac
  done

  ensure_tool jq
  ensure_generator_env

  mkdir -p "$(dirname "$output_file")"
  mkdir -p "$(dirname "$actions_only")"

  # shellcheck disable=SC1090
  source "$GENERATOR_VENV/bin/activate"
  fluxa "$tutorial_url" -o "$output_file"
  jq '.actions' "$output_file" > "$actions_only"
  deactivate || true

  echo "[generate] Full action JSON saved to $output_file"
  echo "[generate] Executable payload saved to $actions_only"

  GENERATED_ACTIONS_PATH="$actions_only"
}

run_apply() {
  if [ $# -lt 2 ]; then
    echo "Error: image paths and action JSON path are required for apply command." >&2
    usage
    exit 1
  fi

  local image_paths="$1"
  local action_json="$2"
  shift 2
  local output_path=""

  while [ $# -gt 0 ]; do
    case "$1" in
      --output|-o)
        output_path="$2"
        shift 2
        ;;
      *)
        echo "Unknown apply option: $1" >&2
        exit 1
        ;;
    esac
  done

  ensure_generator_env

  if [ ! -f "$action_json" ]; then
    echo "Error: action JSON file not found at $action_json" >&2
    exit 1
  fi

  # shellcheck disable=SC1090
  source "$GENERATOR_VENV/bin/activate"
  if [ -n "$output_path" ]; then
    python "$REPO_ROOT/actions.py" "$image_paths" "$action_json" "$output_path"
  else
    python "$REPO_ROOT/actions.py" "$image_paths" "$action_json"
  fi
  deactivate || true
}

run_pipeline() {
  if [ $# -lt 2 ]; then
    echo "Error: tutorial URL and image paths are required for pipeline command." >&2
    usage
    exit 1
  fi

  local tutorial_url="$1"
  local image_paths="$2"
  shift 2

  local json_output="$DEFAULT_JSON_OUTPUT"
  local actions_only="$DEFAULT_ACTIONS_ONLY"
  local render_output=""

  while [ $# -gt 0 ]; do
    case "$1" in
      --json-output)
        json_output="$2"
        shift 2
        ;;
      --actions-only)
        actions_only="$2"
        shift 2
        ;;
      --output|-o|--psd-output)
        render_output="$2"
        shift 2
        ;;
      *)
        echo "Unknown pipeline option: $1" >&2
        exit 1
        ;;
    esac
  done

  run_generate "$tutorial_url" --output "$json_output" --actions-only "$actions_only"
  local actions_path="$GENERATED_ACTIONS_PATH"

  if [ -n "$render_output" ]; then
    run_apply "$image_paths" "$actions_path" --output "$render_output"
  else
    run_apply "$image_paths" "$actions_path"
  fi
}

run_serve() {
  local host="0.0.0.0"
  local port="8000"
  local reload="false"

  while [ $# -gt 0 ]; do
    case "$1" in
      --host)
        host="$2"
        shift 2
        ;;
      --port|-p)
        port="$2"
        shift 2
        ;;
      --reload)
        reload="true"
        shift
        ;;
      *)
        echo "Unknown serve option: $1" >&2
        exit 1
        ;;
    esac
  done

  ensure_generator_env
  # shellcheck disable=SC1090
  source "$GENERATOR_VENV/bin/activate"
  pushd "$REPO_ROOT" >/dev/null
  local uvicorn_args=(server.main:app "--host" "$host" "--port" "$port")
  if [ "$reload" = "true" ]; then
    uvicorn_args+=("--reload")
  fi
  uvicorn "${uvicorn_args[@]}"
  popd >/dev/null
  deactivate || true
}

main() {
  if [ $# -eq 0 ]; then
    usage
    exit 1
  fi

  case "$1" in
    setup)
      shift
      run_setup "$@"
      ;;
    generate)
      shift
      run_generate "$@"
      ;;
    apply)
      shift
      run_apply "$@"
      ;;
    pipeline)
      shift
      run_pipeline "$@"
      ;;
    serve)
      shift
      run_serve "$@"
      ;;
    *)
      if [ $# -ge 2 ]; then
        echo "[info] Falling back to legacy pipeline invocation"
        run_pipeline "$@"
      else
        usage
        exit 1
      fi
      ;;
  esac
}

main "$@"
