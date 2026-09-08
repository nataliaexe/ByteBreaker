#  BYTEBREAKER Framework

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-16%2F16%20PASS-brightgreen.svg)](tests/)
[![Modules](https://img.shields.io/badge/Modules-8-orange.svg)](modules/)
[![Agents](https://img.shields.io/badge/Agents-3-purple.svg)](agents/)
[![API](https://img.shields.io/badge/API-FastAPI-teal.svg)](api/)
[![Docker](https://img.shields.io/badge/Docker-Supported-blue.svg)](Dockerfile)

**Advanced Penetration Testing Framework** with 8 integrated modules, 3 autonomous agents, machine learning detection, and a complete testing laboratory.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Modules](#modules)
- [Agents](#agents)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
- [API Reference](#api-reference)
- [Testing](#testing)
- [Laboratory](#laboratory)
- [Security & Ethics](#security--ethics)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

ByteBreaker is a comprehensive penetration testing framework that combines multiple security testing tools into a unified platform. Designed for security professionals, CTF players, and cybersecurity students.

### Why ByteBreaker?

- **Multi-functional**: 8 tools in 1 framework
- **Autonomous**: 3 agents for continuous monitoring
- **Professional**: Production-ready code quality
- **Educational**: Built-in vulnerable lab for safe testing
- **Extensible**: Modular architecture for easy expansion

---

## Features

### Core Capabilities

-  **Multi-threaded port scanning**
-  **OS fingerprinting** (TTL + header analysis)
-  **Directory bruteforce**
-  **SQL Injection detection**
-  **XSS detection**
-  **Hash cracking** (MD5, SHA1, SHA256)
-  **Metadata extraction**
-  **Network sniffing**
-  **Machine Learning** for threat classification
-  **Real-time dashboard**
-  **Reports**: JSON, HTML, PDF

### Advanced Features

- **Authorization Management**: Scope-based access control
- **Action Logging**: Complete audit trail
- **Rate Limiting**: Prevents abuse
- **Safe Mode**: Simulated exploitation
- **Async Operations**: Non-blocking I/O
- **Concurrent Scanning**: Thread pool management

---

##  Architecture

```
bytebreaker/
│
├── core/                    # Core engine
│   ├── engine.py            # Main orchestrator
│   ├── engine_v2.py         # Enhanced engine (8 modules)
│   ├── config.py            # Configuration management
│   ├── authorization.py     # Access control
│   └── logger.py            # Multi-handler logging
│
├── modules/                 # 8 Security Modules
│   ├── recon.py             # ReconX - Reconnaissance
│   ├── scanner.py           # VulnScan - Vulnerability Scanner
│   ├── exploit.py           # ExploitLab - Controlled Exploitation
│   ├── cracker.py           # HashCrack - Hash Cracking
│   ├── forensics.py         # ForensicKit - Forensic Analysis
│   ├── dir_bruteforce.py    # Directory Bruteforce
│   ├── network_sniffer.py   # Network Analysis
│   └── os_fingerprint.py    # OS Detection
│
├── agents/                  # 3 Autonomous Agents
│   ├── crawler/             # Web Crawler Agent
│   ├── osint/               # OSINT Agent
│   └── monitor/             # Threat Monitor Agent
│
├── utils/                   # Utilities
│   ├── network.py           # Network operations
│   ├── crypto.py            # Cryptographic functions
│   ├── ml.py                # Machine Learning
│   ├── database.py          # Data persistence
│   └── pdf_report.py        # PDF generation
│
├── cli/                     # Command-line Interface
│   ├── main.py              # Standard CLI
│   ├── main_v2.py           # Enhanced CLI (all modules)
│   └── interactive.py       # Interactive console
│
├── api/                     # REST API
│   ├── server.py            # FastAPI server
│   ├── routes.py            # API routes
│   └── dashboard.py         # Web dashboard
│
├── lab/                     # Testing Laboratory
│   ├── services/            # Vulnerable services
│   ├── data/                # Test data & wordlists
│   └── scripts/             # Test scripts
│
├── templates/               # Web templates
├── tests/                   # Unit tests (16/16)
├── docs/                    # Documentation
└── data/                    # Runtime data
```

---

##  Modules

### 1. ReconX - Reconnaissance

**Port scanning, DNS enumeration, WHOIS lookup, SSL analysis**

```bash
python cli/main.py recon --target example.com --options '{"port_scan": true}'
```

**Features:**
- Concurrent port scanning (19 common ports)
- DNS record enumeration (A, AAAA, MX, NS, TXT, SOA, CNAME)
- WHOIS information gathering
- SSL/TLS certificate analysis
- Service identification

---

### 2. VulnScan - Vulnerability Scanner

**SQLi, XSS, security headers, sensitive files**

```bash
python cli/main.py scan --target example.com --type web
```

**Detection Capabilities:**
- SQL Injection (8 payload types)
- XSS (5 payload types)
- Missing security headers (6 checks)
- Sensitive file exposure (10+ patterns)
- Directory listing

---

### 3. ExploitLab - Controlled Exploitation

**Safe-mode exploitation with simulation**

```bash
python cli/main.py exploit --target example.com --name command_injection
```

**Available Exploits:**
- Command Injection (5 payloads)
- Path Traversal (4 payloads)
- File Upload testing

**Safety Features:**
- Safe mode enabled by default
- Target whitelist required
- Action logging

---

### 4. HashCrack - Hash Cracking

**MD5, SHA1, SHA256 cracking with wordlists**

```bash
python cli/main.py crack --hash <hash> --type md5 --wordlist wordlist.txt
```

**Capabilities:**
- Multiple hash algorithms
- Custom wordlist support
- Common password checking (25 defaults)
- Fast cracking (1000s/sec)

---

### 5. ForensicKit - Forensic Analysis

**File hashing, metadata, strings extraction**

```bash
python cli/main.py forensics --file suspicious.exe --type full
```

**Analysis Types:**
- Hash calculation (MD5, SHA1, SHA256)
- Metadata extraction
- String extraction (ASCII)
- Suspicious indicator detection
- File type identification

---

### 6. DirBruteforce - Directory Discovery

```bash
python cli/main_v2.py dirb --target example.com
```

**Checks:** 20+ common paths (admin, backup, config, etc.)

---

### 7. NetworkSniffer - Network Analysis

```bash
python cli/main_v2.py sniff --interface eth0 --count 100
```

**Uses Scapy for packet capture and analysis**

---

### 8. OSFingerprint - OS Detection

```bash
python cli/main_v2.py fingerprint --target example.com
```

**Techniques:** TTL analysis, server header analysis

---

##  Agents

### WebCrawler Agent
Autonomously crawls websites extracting:
- Page titles and metadata
- Forms and inputs
- Email addresses
- Links and scripts

### OSINT Agent
Gathers open-source intelligence:
- DNS records
- WHOIS information
- Subdomain discovery
- Technology detection
- IP geolocation

### ThreatMonitor Agent
Continuous monitoring:
- Security header checks
- Uptime monitoring
- Threat detection
- Alert generation

---

##  Quick Start

### Prerequisites
- Python 3.8+
- pip
- git

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/bytebreaker.git
cd bytebreaker

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### First Steps

```bash
# 1. Authorize target (required)
python cli/main.py authorize --target example.com --scope recon,scan --by "Your Name"

# 2. Run reconnaissance
python cli/main.py recon --target example.com

# 3. Scan for vulnerabilities
python cli/main.py scan --target example.com --type web

# 4. Generate report
python cli/main.py report --format json
```

---

##  Usage Examples

### Complete Workflow

```bash
# 1. Authorization
python cli/main.py authorize --target example.com --scope recon,scan,exploit --by "Name" --days 30

# 2. Reconnaissance
python cli/main.py recon --target example.com --options '{"port_scan": true, "ssl_check": true}'

# 3. Vulnerability Scan
python cli/main.py scan --target example.com --type full

# 4. Directory Bruteforce
python cli/main_v2.py dirb --target example.com

# 5. OS Fingerprinting
python cli/main_v2.py fingerprint --target example.com

# 6. Exploitation (simulated)
python cli/main.py exploit --target example.com --name command_injection

# 7. Report Generation
python cli/main.py report --format json
python cli/main.py report --format html
python cli/main_v2.py pdf
```

### Hash Cracking Examples

```bash
# MD5
python cli/main.py crack --hash 5f4dcc3b5aa765d61d8327deb882cf99 --type md5

# SHA256 with wordlist
python cli/main.py crack --hash <hash> --type sha256 --wordlist wordlist.txt

# Complex password
python cli/main.py crack --hash <hash> --type md5 --wordlist custom_wordlist.txt
```

### Forensic Analysis

```bash
# Full analysis
python cli/main.py forensics --file file.txt --type full

# Hash only
python cli/main.py forensics --file file.txt --type hash

# Metadata only
python cli/main.py forensics --file file.txt --type metadata
```

---

##  API Reference

### Start API Server

```bash
python3 -m uvicorn api.server:app --host 0.0.0.0 --port 8000
```

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info |
| GET | `/status` | Framework status |
| POST | `/authorize` | Add authorization |
| GET | `/authorizations` | List authorizations |
| POST | `/recon` | Run reconnaissance |
| POST | `/scan` | Run vulnerability scan |
| POST | `/crack` | Crack hash |
| POST | `/forensics` | Run forensic analysis |
| GET | `/report` | Generate report |

### Example

```bash
curl -X POST http://localhost:8000/crack \
  -H "Content-Type: application/json" \
  -d '{"hash": "5f4dcc3b5aa765d61d8327deb882cf99", "hash_type": "md5"}'
```

---

##  Testing

### Run All Tests

```bash
./full_test.sh
```

### Results

```
Testes passaram: 16
Testes falharam: 0
TODOS OS TESTES PASSARAM!
```

### Test Coverage

- Core imports
- Configuration validation
- Authorization system
- All 8 modules
- API endpoints
- Interactive mode
- Web dashboard
- Agents
- Laboratory

---

##  Laboratory

### Included Vulnerable Services

A complete testing laboratory with intentionally vulnerable web server:

**Vulnerabilities:**
- XSS (reflected)
- SQL Injection
- Path Traversal
- Directory Listing
- Sensitive File Exposure

### Start Laboratory

```bash
./lab/restart_server.sh
```

### Test Data

- Custom wordlists (12-43 passwords)
- Sample files for forensics
- Pre-computed hashes

---

##  Security & Ethics

### Disclaimer

**This framework is for educational and authorized testing purposes only.**

### Ethical Guidelines

1. **Always obtain authorization** before testing
2. **Use in controlled environments** only
3. **Respect all laws** and regulations
4. **Document all activities**
5. **Keep audit logs**

### Safety Features

- Authorization required for all operations
- Safe mode for exploitation
- Action logging for audit
- Rate limiting
- Input validation

---

## Contributing

### How to Contribute

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

##  License

Distributed under the MIT License. See `LICENSE` for more information.

---

##  Contact

Email: .[nataliavargas.exe@gmail.com](nataliavargas.exe@gmail.com)
Project Link: [https://github.com/nataliaexe/bytebreaker](https://github.com/nataliaexe/bytebreaker)

---

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [Scapy](https://scapy.net/)
- [aiohttp](https://docs.aiohttp.org/)
- [dnspython](https://www.dnspython.org/)
- [ReportLab](https://www.reportlab.com/)

---

