# ByteBreaker Usage Guide

## Installation

### Prerequisites
- Python 3.8+
- pip
- Git

### Setup
```bash
# Clone repository
git clone https://github.com/yourusername/bytebreaker.git
cd bytebreaker

# Install dependencies
pip install -r requirements.txt

# Create directories
mkdir -p data/{wordlists,reports,logs} models
Command Line Usage
Getting Help
bash

python cli/main.py --help

Authorizing Targets
bash

# Authorize for recon and scan
python cli/main.py authorize --target example.com --scope recon,scan --by "Your Name"

# Authorize for exploit (use carefully)
python cli/main.py authorize --target example.com --scope recon,scan,exploit --by "Your Name" --days 7

Reconnaissance
bash

# Basic recon
python cli/main.py recon --target example.com

# With specific options
python cli/main.py recon --target example.com --options '{"port_scan": true, "ssl_check": true}'

Vulnerability Scanning
bash

# Full scan
python cli/main.py scan --target example.com --type full

# Quick scan
python cli/main.py scan --target example.com --type quick

# Web scan only
python cli/main.py scan --target example.com --type web

Exploitation (Simulated)
bash

# List available exploits
# (Use with proper authorization only)
python cli/main.py exploit --target example.com --name command_injection

Hash Cracking
bash

# Crack MD5 hash
python cli/main.py crack --hash 5f4dcc3b5aa765d61d8327deb882cf99 --type md5

# With custom wordlist
python cli/main.py crack --hash <hash> --type sha256 --wordlist /path/to/wordlist.txt

Forensic Analysis
bash

# Full analysis
python cli/main.py forensics --file suspicious.exe --type full

# Hash only
python cli/main.py forensics --file suspicious.exe --type hash

# Metadata only
python cli/main.py forensics --file suspicious.exe --type metadata

Reports
bash

# Generate JSON report
python cli/main.py report --format json

# Generate HTML report
python cli/main.py report --format html

Status
bash

# Check framework status
python cli/main.py status

# List authorizations
python cli/main.py authorizations

API Usage
Starting API Server
bash

# Start API server
python -m uvicorn api.server:app --host 0.0.0.0 --port 8000

API Examples
bash

# Get status
curl http://localhost:8000/status

# Authorize target
curl -X POST http://localhost:8000/authorize \
  -H "Content-Type: application/json" \
  -d '{"target": "example.com", "scope": ["recon"], "authorized_by": "John"}'

# Run recon
curl -X POST http://localhost:8000/recon \
  -H "Content-Type: application/json" \
  -d '{"target": "example.com"}'

Best Practices
Safety

    Always obtain written authorization

    Test only in controlled environments

    Respect rate limits

    Use safe mode when possible

Performance

    Adjust thread counts based on network

    Use appropriate scan types

    Monitor resource usage

    Clean up after operations

Legal

    Comply with all applicable laws

    Respect privacy

    Document all activities

    Keep audit logs

Troubleshooting
Common Issues

    Permission errors: Check authorization

    Network timeouts: Adjust timeout settings

    Module errors: Check dependencies

    Database errors: Check permissions

Debug Mode
bash

# Enable debug logging
export BYTEBREAKER_DEBUG=1
python cli/main.py ...

