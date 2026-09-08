#!/bin/bash

echo "=== Executando testes do ByteBreaker ==="

# Ativar venv
source venv/bin/activate

# Teste 1: Autorização
echo -e "\n[1/5] Testando autorização..."
python cli/main.py authorize --target 127.0.0.1 --scope recon,scan --by "Lab Test" --days 1

# Teste 2: Reconhecimento
echo -e "\n[2/5] Testando reconhecimento..."
python cli/main.py recon --target 127.0.0.1 --options '{"port_scan": true, "ssl_check": false}'

# Teste 3: Scanner
echo -e "\n[3/5] Testando scanner..."
python cli/main.py scan --target 127.0.0.1 --type quick

# Teste 4: Hash cracking
echo -e "\n[4/5] Testando hash cracking..."
HASH=$(cat lab/data/test_hash.txt)
python cli/main.py crack --hash $HASH --type md5

# Teste 5: Forensics
echo -e "\n[5/5] Testando forensics..."
python cli/main.py forensics --file lab/data/forensics_test.txt --type full

echo -e "\n=== Testes completos ==="
python cli/main.py report --format json
echo "Relatório gerado em: data/reports/"
