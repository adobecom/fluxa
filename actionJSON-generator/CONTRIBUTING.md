# Contributing to Fluxa

Thank you for your interest in contributing to Fluxa! This document provides guidelines and information for contributors.

## Development Setup

1. **Fork and clone the repository**

2. **Set up the development environment**:
   ```bash
   cd Fluxa
   python3.10 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install -e ".[dev]"
   ```

3. **Set up your OpenAI API key** for testing:
   ```bash
   cp .env.example .env
   # Edit .env and add your key
   ```

## Project Structure

```
Fluxa/
├── src/fluxa/
│   ├── extractors/       # Content extraction modules
│   ├── generators/       # AI generation logic
│   ├── prompts/          # AI prompt templates
│   ├── utils/            # Validation and formatting
│   ├── knowledge/        # Photoshop operations knowledge base
│   └── cli.py           # CLI interface
├── config/              # Configuration files
├── examples/            # Example outputs and usage
├── tests/               # Test suite
└── docs/                # Additional documentation
```

## Areas for Contribution

### 1. Photoshop Operations Knowledge Base

The knowledge base in `src/fluxa/knowledge/photoshop_operations.json` can be expanded with:
- More Photoshop operations (filters, adjustments, etc.)
- Better parameter validation rules
- More detailed examples

### 2. Prompt Engineering

Improve the AI prompts in `src/fluxa/prompts/photoshop_actions.py`:
- Better few-shot examples
- More specific instructions
- Handling edge cases

### 3. Validation

Enhance validation in `src/fluxa/utils/validator.py`:
- More comprehensive checks
- Better error messages
- Support for more operations

### 4. Content Extraction

Improve extractors in `src/fluxa/extractors/`:
- Better web scraping heuristics
- Support for more video platforms
- PDF tutorial support

### 5. Testing

Add tests in `tests/`:
- Unit tests for extractors
- Integration tests
- Mock AI responses for deterministic testing

## Code Style

- Follow PEP 8
- Use type hints
- Document functions with docstrings
- Use Black for formatting: `black src/`
- Use mypy for type checking: `mypy src/`

## Testing

Run tests before submitting:
```bash
pytest tests/
```

## Submitting Changes

1. Create a feature branch
2. Make your changes
3. Add tests if applicable
4. Run tests and linting
5. Submit a pull request with a clear description

## Questions?

Feel free to open an issue for discussion before starting major work.


