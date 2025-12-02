#!/bin/bash

# Fluxa Setup Script
# Sets up the Python environment and installs dependencies

set -e

echo "🎨 Setting up Fluxa AI Tool..."
echo ""

# Check Python version
echo "Checking Python version..."
if ! command -v python3.10 &> /dev/null; then
    echo "❌ Python 3.10 not found. Please install Python 3.10 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3.10 --version | cut -d' ' -f2)
echo "✓ Found Python $PYTHON_VERSION"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3.10 -m venv venv
echo "✓ Virtual environment created"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo "✓ pip upgraded"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Install Fluxa in editable mode
echo "Installing Fluxa..."
pip install -e .
echo "✓ Fluxa installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cat > .env << 'EOF'
# OpenAI API Configuration
OPENAI_API_KEY=your_api_key_here

# Optional: Override default model
# OPENAI_MODEL=gpt-4o

# Optional: Set API timeout (seconds)
# API_TIMEOUT=60
EOF
    echo "✓ .env file created"
    echo ""
    echo "⚠️  Please edit .env and add your OpenAI API key"
else
    echo "✓ .env file already exists"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Add your OpenAI API key to .env file"
echo "3. Run: fluxa --help"
echo ""
echo "Example usage:"
echo "  fluxa https://www.youtube.com/watch?v=VIDEO_ID -o output.json"
echo ""


