# Fluxa Project Summary

## Overview

**Fluxa** is a complete AI-powered CLI tool that converts Photoshop tutorials into executable Photoshop API JSON action files. Built with Python 3.10 and powered by OpenAI GPT-4o.

## Architecture

### Core Components

1. **Content Extractors** (`src/fluxa/extractors/`)
   - `YouTubeExtractor`: Extracts transcripts from YouTube videos
   - `WebExtractor`: Scrapes and processes web articles
   - `ExtractorFactory`: Routes URLs to appropriate extractors

2. **AI Generator** (`src/fluxa/generators/`)
   - `PhotoshopActionGenerator`: Uses OpenAI GPT-4o to convert tutorial text into Photoshop API JSON
   - Includes retry logic, cost estimation, and response validation

3. **Prompt Engineering** (`src/fluxa/prompts/`)
   - Carefully crafted system and user prompts
   - Few-shot examples for better AI understanding
   - Based on actual Photoshop API JSON format

4. **Knowledge Base** (`src/fluxa/knowledge/`)
   - `photoshop_operations.json`: Catalog of supported Photoshop operations
   - Includes structure templates, examples, and parameter documentation
   - Extracted from the existing Action.json in the parent project

5. **Validation & Formatting** (`src/fluxa/utils/`)
   - `ActionValidator`: Validates generated JSON against Photoshop API specs
   - `formatter`: Pretty-prints JSON and adds metadata
   - Parameter range checking for operations like emboss

6. **CLI Interface** (`src/fluxa/cli.py`)
   - Built with Click and Rich for beautiful terminal UI
   - Progress indicators, cost estimates, and verbose output
   - Comprehensive error handling

## Features Implemented

✅ **YouTube Support**: Automatic transcript extraction  
✅ **Web Article Support**: Smart content scraping  
✅ **AI-Powered Generation**: GPT-4o integration with custom prompts  
✅ **Validation**: Comprehensive JSON validation  
✅ **Cost Estimation**: Preview API costs before running  
✅ **Beautiful CLI**: Rich terminal output with progress indicators  
✅ **Error Handling**: Graceful degradation and helpful error messages  
✅ **Metadata**: Optional metadata wrapper for outputs  
✅ **Configuration**: Flexible config file system  
✅ **Testing**: Unit tests for core components  
✅ **Documentation**: Complete README, quickstart, and examples  

## Project Structure

```
Fluxa/
├── src/fluxa/                    # Main source code
│   ├── extractors/               # Content extraction
│   │   ├── youtube_extractor.py
│   │   ├── web_extractor.py
│   │   └── factory.py
│   ├── generators/               # AI generation
│   │   └── photoshop_action_generator.py
│   ├── prompts/                  # AI prompts
│   │   └── photoshop_actions.py
│   ├── knowledge/                # Photoshop operations DB
│   │   └── photoshop_operations.json
│   ├── utils/                    # Utilities
│   │   ├── validator.py
│   │   └── formatter.py
│   └── cli.py                    # CLI interface
├── config/                       # Configuration
│   └── default.json
├── examples/                     # Example usage
│   ├── example-output.json
│   ├── example-youtube-url.txt
│   └── example-web-url.txt
├── tests/                        # Test suite
│   ├── test_validator.py
│   └── test_extractors.py
├── README.md                     # Main documentation
├── QUICKSTART.md                 # Quick start guide
├── CONTRIBUTING.md               # Contribution guide
├── requirements.txt              # Python dependencies
├── pyproject.toml               # Package configuration
└── setup.sh                     # Setup script
```

## Dependencies

### Core Dependencies
- `openai>=1.0.0` - OpenAI API integration
- `youtube-transcript-api>=0.6.0` - YouTube transcript extraction
- `beautifulsoup4>=4.12.0` - Web scraping
- `requests>=2.31.0` - HTTP requests
- `click>=8.1.0` - CLI framework
- `rich>=13.0.0` - Terminal formatting
- `python-dotenv>=1.0.0` - Environment configuration
- `lxml>=4.9.0` - HTML parsing

### Dev Dependencies
- `pytest>=7.0.0` - Testing
- `black>=23.0.0` - Code formatting
- `mypy>=1.0.0` - Type checking

## Usage Examples

### Basic Usage
```bash
# From YouTube
fluxa https://www.youtube.com/watch?v=VIDEO_ID -o output.json

# From web article
fluxa https://example.com/tutorial -o output.json
```

### Advanced Usage
```bash
# With verbose output and cost estimate
fluxa URL -v --estimate-cost

# Without metadata wrapper
fluxa URL --no-metadata -o clean.json

# Using specific model
fluxa URL -m gpt-4-turbo -o output.json
```

## Installation

### Quick Setup
```bash
cd Fluxa
bash setup.sh
export OPENAI_API_KEY='your-key-here'
fluxa --help
```

### Manual Setup
```bash
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Output Format

The tool generates Photoshop API-compatible JSON for use in API contexts (where documents are already loaded):

```json
{
  "_metadata": {
    "generated_by": "Fluxa AI Tool",
    "generated_at": "2024-01-15T10:30:00Z",
    "source": "https://youtube.com/...",
    "source_type": "youtube"
  },
  "actions": [
    {"_obj": "emboss", "amount": 100, "angle": 135, "height": 3},
    {"_obj": "set", "_target": [{"_enum": "ordinal", "_ref": "layer"}], "to": {"_obj": "layer", "opacity": {"_unit": "percentUnit", "_value": 75.0}}}
  ]
}
```

**Note**: File I/O operations (`open`, `save`) are excluded as the Photoshop API operates on documents that are already loaded in memory.

## Supported Operations

- **Layer**: make, delete, select, show, hide, move, set
- **Filters**: emboss (more can be added)
- **Color**: fill, reset, exchange
- **Document**: close (when needed)
- Plus many more documented in the knowledge base

**Excluded**: File I/O operations requiring filesystem access (`open`, `save`, and operations with local file paths)

## Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=fluxa
```

## Future Enhancements

Potential areas for expansion:
- Support for more Photoshop operations
- PDF tutorial parsing
- Video platform support beyond YouTube
- Batch processing of multiple tutorials
- Interactive mode for refining outputs
- Integration with the visual composer (parent project)

## Integration with Parent Project

Fluxa is designed to complement the existing actionJSON-composer:
- Uses the same Photoshop API JSON format
- Can generate inputs for the visual composer
- Extracts operation knowledge from existing Action.json
- Provides an alternative creation method (AI vs visual)

## Success Metrics

The tool successfully:
1. ✅ Extracts content from YouTube and web tutorials
2. ✅ Generates valid Photoshop API JSON
3. ✅ Validates output with helpful error messages
4. ✅ Provides cost-transparent AI usage
5. ✅ Handles errors gracefully
6. ✅ Offers comprehensive documentation

## Credits

Built as part of the actionJSON-composer project using:
- OpenAI GPT-4o for AI generation
- youtube-transcript-api for YouTube support
- Beautiful Soup for web scraping
- Click and Rich for CLI interface


