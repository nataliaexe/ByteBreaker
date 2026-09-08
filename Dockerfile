FROM python:3.9-slim

LABEL maintainer="Your Name <your.email@example.com>"
LABEL description="ByteBreaker - Advanced Pentest Framework"
LABEL version="1.0.0"

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpcap-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data/wordlists data/reports data/logs models

# Create non-root user
RUN useradd -m -s /bin/bash bytebreaker && \
    chown -R bytebreaker:bytebreaker /app
USER bytebreaker

# Expose API port
EXPOSE 8000

# Default command
CMD ["python", "cli/main.py", "--help"]
