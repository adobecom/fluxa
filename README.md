# Photoshop API Executor

A general-purpose tool to execute Photoshop actions defined in JSON files on images using the Adobe Photoshop API.

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
