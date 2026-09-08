#!/bin/bash

# ByteBreaker Installation Script
echo "Starting ByteBreaker Installation..."

# Check Python version
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
if (( $(echo "$python_version < 3.8" | bc -l) )); then
    echo "Error: Python 3.8+ is required"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create directories
echo "Creating directories..."
mkdir -p data/wordlists data/reports data/logs models

# Create default config
if [ ! -f config.json ]; then
    echo "Creating default config..."
    cp config.json.example config.json 2>/dev/null || echo '{}' > config.json
fi

# Set permissions
echo "Setting permissions..."
chmod +x cli/main.py

echo "Installation complete!"
echo "Activate virtual environment: source venv/bin/activate"
echo "Run: python cli/main.py --help"
