#!/usr/bin/env python3
"""
Fluxa Setup Verification Script
Checks that all components are properly installed and configured
"""

import sys
import os
from pathlib import Path


def check_file_exists(path: str, description: str) -> bool:
    """Check if a file exists"""
    if Path(path).exists():
        print(f"✓ {description}")
        return True
    else:
        print(f"✗ {description} - MISSING")
        return False


def check_python_version() -> bool:
    """Check Python version"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 10:
        print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python version: {version.major}.{version.minor}.{version.micro} - Need 3.10+")
        return False


def check_imports() -> bool:
    """Check if key dependencies can be imported"""
    try:
        import openai
        print("✓ openai package installed")
    except ImportError:
        print("✗ openai package not found")
        return False
    
    try:
        import click
        print("✓ click package installed")
    except ImportError:
        print("✗ click package not found")
        return False
    
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        print("✓ youtube-transcript-api package installed")
    except ImportError:
        print("✗ youtube-transcript-api package not found")
        return False
    
    try:
        from bs4 import BeautifulSoup
        print("✓ beautifulsoup4 package installed")
    except ImportError:
        print("✗ beautifulsoup4 package not found")
        return False
    
    try:
        from rich.console import Console
        print("✓ rich package installed")
    except ImportError:
        print("✗ rich package not found")
        return False
    
    return True


def check_env_vars() -> bool:
    """Check environment variables"""
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key and api_key != 'your_api_key_here':
        print("✓ OPENAI_API_KEY environment variable set")
        return True
    else:
        print("⚠ OPENAI_API_KEY not set (you'll need this to run Fluxa)")
        return False


def main():
    """Run all checks"""
    print("=" * 60)
    print("Fluxa Setup Verification")
    print("=" * 60)
    print()
    
    all_good = True
    
    # Check Python version
    print("Checking Python version...")
    if not check_python_version():
        all_good = False
    print()
    
    # Check core files
    print("Checking core files...")
    base = Path(__file__).parent
    files_to_check = [
        (base / "src/fluxa/__init__.py", "Main package"),
        (base / "src/fluxa/cli.py", "CLI module"),
        (base / "src/fluxa/extractors/youtube_extractor.py", "YouTube extractor"),
        (base / "src/fluxa/extractors/web_extractor.py", "Web extractor"),
        (base / "src/fluxa/generators/photoshop_action_generator.py", "AI generator"),
        (base / "src/fluxa/utils/validator.py", "Validator"),
        (base / "src/fluxa/knowledge/photoshop_operations.json", "Knowledge base"),
        (base / "config/default.json", "Configuration"),
        (base / "requirements.txt", "Requirements file"),
    ]
    
    for filepath, desc in files_to_check:
        if not check_file_exists(filepath, desc):
            all_good = False
    print()
    
    # Check dependencies
    print("Checking dependencies...")
    if not check_imports():
        all_good = False
    print()
    
    # Check environment
    print("Checking environment...")
    check_env_vars()  # Don't fail on missing API key, just warn
    print()
    
    # Final verdict
    print("=" * 60)
    if all_good:
        print("✅ All checks passed! Fluxa is ready to use.")
        print()
        print("Next steps:")
        print("1. Set your OpenAI API key: export OPENAI_API_KEY='your-key'")
        print("2. Run: fluxa --help")
        print("3. Try: fluxa <tutorial-url> -o output.json")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print()
        print("Try running: bash setup.sh")
    print("=" * 60)
    
    return 0 if all_good else 1


if __name__ == "__main__":
    sys.exit(main())


