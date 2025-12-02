# Fluxa AI Tool

🎨 **Fluxa** is an AI-powered CLI tool that converts Photoshop tutorials (from YouTube videos or web articles) into executable Photoshop API JSON action files.

## Features

- ✨ **AI-Powered**: Uses OpenAI GPT-4o to understand and convert tutorial content
- 🎥 **YouTube Support**: Extracts transcripts from YouTube tutorial videos
- 🌐 **Web Article Support**: Scrapes and processes web-based tutorials
- ✅ **Validation**: Validates generated JSON against Photoshop API specifications
- 💰 **Cost Estimation**: Preview API costs before processing
- 🎯 **Smart Extraction**: Automatically identifies and extracts Photoshop-specific operations

## Installation

### Requirements

- Python 3.10 or higher
- OpenAI API key

### Setup

1. **Clone or navigate to the Fluxa directory**:
   ```bash
   cd Fluxa
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Fluxa**:
   ```bash
   pip install -e .
   ```

5. **Configure your OpenAI API key**:
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

   Or export it as an environment variable:
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

## Usage

### Basic Usage

Convert a YouTube tutorial to Photoshop API JSON:

```bash
fluxa https://www.youtube.com/watch?v=VIDEO_ID
```

Convert a web article tutorial:

```bash
fluxa https://example.com/photoshop-tutorial
```

### Options

```bash
fluxa [URL] [OPTIONS]

Options:
  -o, --output PATH       Output file path (default: output.json)
  -m, --model TEXT       OpenAI model to use (default: gpt-4o)
  --api-key TEXT         OpenAI API key (or set OPENAI_API_KEY env variable)
  -v, --verbose          Show detailed processing information
  --no-metadata          Do not add metadata to output
  --no-validate          Skip validation
  --estimate-cost        Show cost estimate and exit without generating
  --help                 Show this message and exit
```

### Examples

**Generate with custom output file**:
```bash
fluxa https://youtube.com/watch?v=... -o my-actions.json
```

**Show verbose output and cost estimate**:
```bash
fluxa https://example.com/tutorial -v --estimate-cost
```

**Use a different model**:
```bash
fluxa https://youtube.com/watch?v=... -m gpt-4-turbo
```

**Generate without metadata wrapper**:
```bash
fluxa https://example.com/tutorial --no-metadata -o clean-actions.json
```

## Output Format

**Important Note about API Context**: Fluxa generates actions for use with the Photoshop API, which operates on documents that are already loaded in memory. Therefore, generated actions **exclude** filesystem operations like `open` and `save`. The API caller is responsible for:
- Loading the source document before executing the actions
- Retrieving/saving the result after execution

### With Metadata (Default)

```json
{
  "_metadata": {
    "generated_by": "Fluxa AI Tool",
    "generated_at": "2024-01-15T10:30:00Z",
    "version": "0.1.0",
    "source": "https://youtube.com/watch?v=...",
    "source_type": "youtube"
  },
  "actions": [
    {
      "_obj": "emboss",
      "amount": 100,
      "angle": 135,
      "height": 3
    },
    {
      "_obj": "set",
      "_target": [{"_enum": "ordinal", "_ref": "layer"}],
      "to": {
        "_obj": "layer",
        "opacity": {"_unit": "percentUnit", "_value": 75.0}
      }
    }
  ]
}
```

### Without Metadata (--no-metadata)

```json
[
  {
    "_obj": "emboss",
    "amount": 100,
    "angle": 135,
    "height": 3
  },
  {
    "_obj": "make",
    "_target": [{"_ref": "layer"}]
  }
]
```

## Supported Photoshop Operations

Fluxa understands and can generate the following Photoshop API operations:

- **Layer Operations**: `make`, `delete`, `select`, `show`, `hide`, `move`, `set`
- **Filters**: `emboss` (more filters can be added)
- **Color Operations**: `fill`, `reset`, `exchange`
- **Document Operations**: `close` (when needed)
- **And more**: See `src/fluxa/knowledge/photoshop_operations.json` for full list

**Note**: File I/O operations (`open`, `save`) are intentionally excluded as they require filesystem access not available in the Photoshop API context. Operations that reference local file paths (e.g., loading displacement maps or textures) are also omitted.

## Configuration

Edit `config/default.json` to customize:

```json
{
  "openai": {
    "model": "gpt-4o",
    "temperature": 0.1,
    "max_tokens": 4000,
    "timeout": 60
  },
  "output": {
    "indent": 2,
    "add_metadata": true,
    "validate": true
  },
  "extraction": {
    "youtube": {
      "max_transcript_length": 50000
    },
    "web": {
      "max_content_length": 100000,
      "timeout": 30
    }
  }
}
```

## Troubleshooting

### "No transcript found for video"

Some YouTube videos don't have captions/transcripts. Try:
- Finding a different tutorial with captions
- Using a web article instead
- Manually creating a transcript

### "Could not extract video ID from URL"

Ensure you're using a valid YouTube URL format:
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`

### "Validation warnings"

The tool may still generate usable JSON even with validation warnings. Review the output to determine if it meets your needs. Common warnings:
- Unknown operations (may still be valid)
- Parameter out of suggested range (may still work)

### High API Costs

- Use `--estimate-cost` to preview costs before generating
- Consider using shorter tutorials
- The gpt-4o model is cost-effective for this use case

## Development

### Project Structure

```
Fluxa/
├── src/fluxa/
│   ├── extractors/       # Content extraction (YouTube, Web)
│   ├── generators/       # AI-powered JSON generation
│   ├── prompts/          # AI prompt templates
│   ├── utils/            # Validation and formatting utilities
│   ├── knowledge/        # Photoshop operations knowledge base
│   └── cli.py           # CLI interface
├── config/              # Configuration files
├── examples/            # Example outputs
├── tests/               # Test files
├── requirements.txt     # Python dependencies
├── pyproject.toml      # Package configuration
└── README.md           # This file
```

### Running Tests

```bash
pytest tests/
```

### Contributing

Contributions are welcome! Areas for improvement:
- Additional Photoshop operations in knowledge base
- Better validation rules
- Support for more tutorial formats
- Improved prompt engineering

## License

This project is part of the actionJSON-composer POC.

## Credits

- Built with [OpenAI GPT-4](https://openai.com)
- Uses [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api)
- Inspired by the [actionJSON-composer project](https://git.corp.adobe.com/pages/kmikawa/actionJSON-composer/)


