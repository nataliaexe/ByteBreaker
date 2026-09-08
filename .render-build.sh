#!/bin/bash
# Render build script

echo "Starting ByteBreaker build..."

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p data/reports data/logs data/wordlists models

# Create default config if not exists
if [ ! -f config.json ]; then
    echo '{}' > config.json
fi

echo "Build complete!"
