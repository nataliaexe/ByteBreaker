#!/bin/bash

echo "=== ByteBreaker Test Laboratory ==="
echo "Starting vulnerable services..."

# Iniciar servidor web vulnerável em background
python3 lab/services/vulnerable_web.py &
WEB_PID=$!
echo "Vulnerable web server PID: $WEB_PID"

# Criar arquivo de teste para forensics
echo "This is a test file for forensic analysis" > lab/data/forensics_test.txt

# Criar hashes para teste
echo -n "admin123" | md5sum | cut -d' ' -f1 > lab/data/test_hash.txt
echo "MD5 hash of 'admin123': $(cat lab/data/test_hash.txt)"

echo ""
echo "=== Laboratório pronto ==="
echo "Serviços disponíveis:"
echo "  Web vulnerável: http://127.0.0.1:8080"
echo "  Arquivo teste: lab/data/forensics_test.txt"
echo "  Hash teste: $(cat lab/data/test_hash.txt)"
echo ""
echo "Para parar o laboratório:"
echo "  kill $WEB_PID"
echo ""
echo "Comandos de teste:"
echo "  python cli/main.py authorize --target 127.0.0.1 --scope recon,scan --by 'Test'"
echo "  python cli/main.py scan --target 127.0.0.1:8080 --type web"
echo "  python cli/main.py forensics --file lab/data/forensics_test.txt --type full"
echo "  python cli/main.py crack --hash $(cat lab/data/test_hash.txt) --type md5"

# Manter script rodando
wait $WEB_PID
