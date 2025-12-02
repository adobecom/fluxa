TUTORIAL_LINK=$1
IMAGE_PATHS=$2
echo $TUTORIAL_LINK
echo $IMAGE_PATHS
cd actionJSON-generator
touch temp.json
nix-shell --run "fluxa $TUTORIAL_LINK -o output.json && cat output.json | jq .actions > temp.json"
cd ..
nix-shell --run "python actions.py $IMAGE_PATHS actionJSON-generator/temp.json"
