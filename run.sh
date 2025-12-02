#!/bin/bash

# Usage:
#   ./run.sh <youtube_url_or_transcript_path> <image_paths> [--use-agent]
#
# Examples:
#   ./run.sh "https://youtube.com/..." "input_images/girl.jpg" --use-agent
#   ./run.sh "transcript.txt" "input_images/girl.jpg" --use-agent
#   ./run.sh "transcript.txt" "input_images/img1.jpg,input_images/img2.jpg"

INPUT=$1
IMAGE_PATHS=$2
USE_AGENT=$3

echo "Input: $INPUT"
echo "Image Paths: $IMAGE_PATHS"
echo "Use Agent: $USE_AGENT"

cd actionJSON-generator
touch temp.json

# Check if input is a file (transcript) or URL
if [ -f "$INPUT" ] || [ -f "../$INPUT" ]; then
    # Input is a transcript file
    TRANSCRIPT_PATH="$INPUT"
    # If relative path doesn't exist, try with parent directory
    if [ ! -f "$TRANSCRIPT_PATH" ]; then
        TRANSCRIPT_PATH="../$INPUT"
    fi
    
    echo "Using transcript file: $TRANSCRIPT_PATH"
    
    if [ "$USE_AGENT" = "--use-agent" ]; then
        echo "Using agent-based generator..."
        fluxa --transcript "$TRANSCRIPT_PATH" -o output.json --use-agent && cat output.json | jq .actions > temp.json
    else
        echo "Using standard generator..."
        fluxa --transcript "$TRANSCRIPT_PATH" -o output.json && cat output.json | jq .actions > temp.json
    fi
else
    # Input is a URL
    echo "Using URL: $INPUT"
    
    if [ "$USE_AGENT" = "--use-agent" ]; then
        echo "Using agent-based generator..."
        fluxa "$INPUT" -o output.json --use-agent && cat output.json | jq .actions > temp.json
    else
        echo "Using standard generator..."
        fluxa "$INPUT" -o output.json && cat output.json | jq .actions > temp.json
    fi
fi

cd ..
python actions.py $IMAGE_PATHS actionJSON-generator/temp.json
