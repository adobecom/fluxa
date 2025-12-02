# Fluxa Installation Guide

Complete installation instructions for Fluxa AI Tool.

## Prerequisites

- **Python 3.10 or higher**
- **OpenAI API Key** (get one at https://platform.openai.com/)
- **Terminal/Command Line** access
- **Internet connection** (for API calls and package installation)

## Installation Methods

### Method 1: Automated Setup (Recommended)

1. **Navigate to Fluxa directory**:
   ```bash
   cd /path/to/actionJSON-composer/Fluxa
   ```

2. **Run setup script**:
   ```bash
   bash setup.sh
   ```

3. **Activate virtual environment**:
   ```bash
   source venv/bin/activate
   ```

4. **Set your API key**:
   ```bash
   export OPENAI_API_KEY='your-openai-api-key-here'
   ```

5. **Verify installation**:
   ```bash
   python verify_setup.py
   ```

### Method 2: Manual Installation

1. **Create virtual environment**:
   ```bash
   cd /path/to/actionJSON-composer/Fluxa
   python3.10 -m venv venv
   ```

2. **Activate virtual environment**:
   
   On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```
   
   On Windows:
   ```bash
   venv\Scripts\activate
   ```

3. **Upgrade pip**:
   ```bash
   pip install --upgrade pip
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Install Fluxa in development mode**:
   ```bash
   pip install -e .
   ```

6. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

7. **Verify installation**:
   ```bash
   fluxa --help
   ```

## Configuration

### Setting OpenAI API Key

Choose one of these methods:

**Option A: Environment Variable (Recommended)**
```bash
export OPENAI_API_KEY='sk-...'
```

Add to your `~/.bashrc` or `~/.zshrc` for persistence:
```bash
echo 'export OPENAI_API_KEY="sk-..."' >> ~/.zshrc
source ~/.zshrc
```

**Option B: .env File**
```bash
echo 'OPENAI_API_KEY=sk-...' > .env
```

**Option C: Command Line Flag**
```bash
fluxa URL --api-key sk-...
```

### Configuring Defaults

Edit `config/default.json` to customize:

```json
{
  "openai": {
    "model": "gpt-4o",        # AI model to use
    "temperature": 0.1,       # Lower = more consistent
    "max_tokens": 4000,       # Max response length
    "timeout": 60             # Request timeout (seconds)
  },
  "output": {
    "indent": 2,              # JSON indentation
    "add_metadata": true,     # Include metadata in output
    "validate": true          # Validate generated JSON
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

## Verification

### Check Installation

Run the verification script:
```bash
python verify_setup.py
```

Expected output:
```
============================================================
Fluxa Setup Verification
============================================================

Checking Python version...
✓ Python version: 3.10.x

Checking core files...
✓ Main package
✓ CLI module
✓ YouTube extractor
✓ Web extractor
✓ AI generator
✓ Validator
✓ Knowledge base
✓ Configuration
✓ Requirements file

Checking dependencies...
✓ openai package installed
✓ click package installed
✓ youtube-transcript-api package installed
✓ beautifulsoup4 package installed
✓ rich package installed

Checking environment...
✓ OPENAI_API_KEY environment variable set

============================================================
✅ All checks passed! Fluxa is ready to use.
============================================================
```

### Test Run

Try a simple command:
```bash
fluxa --help
```

You should see the help message with all available options.

## Troubleshooting

### "command not found: fluxa"

**Solution**: Ensure virtual environment is activated and Fluxa is installed:
```bash
source venv/bin/activate
pip install -e .
```

### "No module named 'fluxa'"

**Solution**: Install in development mode:
```bash
pip install -e .
```

### "OpenAI API key not found"

**Solution**: Set the environment variable:
```bash
export OPENAI_API_KEY='your-key-here'
```

### "Python version too old"

**Solution**: Install Python 3.10 or higher:
- macOS: `brew install python@3.10`
- Ubuntu: `sudo apt install python3.10`
- Windows: Download from python.org

### Import errors

**Solution**: Reinstall dependencies:
```bash
pip install -r requirements.txt --force-reinstall
```

## Updating

To update Fluxa:

```bash
cd /path/to/Fluxa
source venv/bin/activate
git pull  # if using git
pip install -r requirements.txt --upgrade
```

## Uninstalling

To remove Fluxa:

```bash
cd /path/to/Fluxa
deactivate  # if venv is active
rm -rf venv
```

## Next Steps

After successful installation:

1. **Read the Quick Start**: See [QUICKSTART.md](QUICKSTART.md)
2. **Try an example**: `fluxa <tutorial-url> -o test.json`
3. **Read full docs**: See [README.md](README.md)
4. **Check examples**: Browse [examples/](examples/)

## Getting Help

If you encounter issues:

1. Run `python verify_setup.py` to check setup
2. Check [README.md](README.md) troubleshooting section
3. Review [QUICKSTART.md](QUICKSTART.md) for common patterns
4. Open an issue with error details

## System Requirements

- **OS**: macOS, Linux, or Windows
- **RAM**: 512MB minimum
- **Disk**: 500MB for dependencies
- **Network**: Required for API calls and installation


