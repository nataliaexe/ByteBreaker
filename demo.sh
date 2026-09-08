#!/bin/bash

echo "========================================="
echo "  ByteBreaker Framework - Demonstração"
echo "========================================="

# Ativar ambiente
source venv/bin/activate

echo -e "\n[1/6] Verificando status do sistema..."
python cli/main.py status

echo -e "\n[2/6] Testando reconhecimento..."
python cli/main.py recon --target 127.0.0.1 --options '{"port_scan": true, "ssl_check": false}'

echo -e "\n[3/6] Testando scanner de vulnerabilidades..."
python cli/main.py scan --target 127.0.0.1:8080 --type web

echo -e "\n[4/6] Testando hash cracking..."
HASH=$(python3 -c 'import hashlib; print(hashlib.md5("P@ssw0rd!2024".encode()).hexdigest())')
python cli/main.py crack --hash $HASH --type md5 --wordlist lab/data/custom_wordlist.txt

echo -e "\n[5/6] Testando análise forense..."
python cli/main.py forensics --file lab/services/vulnerable_web.py --type full

echo -e "\n[6/6] Gerando relatório..."
python cli/main.py report --format json

echo -e "\n========================================="
echo "  Demonstração completa!"
echo "========================================="
