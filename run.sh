TUTORIAL_LINK=$1
IMAGE_PATHS=$2
USE_AGENT=$3

echo "Tutorial Link: $TUTORIAL_LINK"
echo "Image Paths: $IMAGE_PATHS"
echo "Use Agent: $USE_AGENT"

cd actionJSON-generator
touch temp.json

# Check if --use-agent flag is provided
if [ "$USE_AGENT" = "--use-agent" ]; then
    echo "Using agent-based generator..."
    fluxa $TUTORIAL_LINK -o output.json --use-agent && cat output.json | jq .actions > temp.json
else
    echo "Using standard generator..."
    fluxa $TUTORIAL_LINK -o output.json && cat output.json | jq .actions > temp.json
fi

cd ..
python actions.py $IMAGE_PATHS actionJSON-generator/temp.json
