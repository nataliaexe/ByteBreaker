#!/bin/bash

echo "========================================="
echo "  ByteBreaker - Teste Completo"
echo "========================================="

# Cores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

PASS=0
FAIL=0

check() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}[PASS]${NC} $1"
        PASS=$((PASS+1))
    else
        echo -e "${RED}[FAIL]${NC} $1"
        FAIL=$((FAIL+1))
    fi
}

# Ativar ambiente
source venv/bin/activate

# 1. Testar imports
echo -e "\n${BLUE}[1/15] Testando imports...${NC}"
python3 -c "
from core.config import Config
from core.logger import ByteBreakerLogger
from core.authorization import AuthorizationManager
from core.engine import Engine
print('Core imports OK')
"
check "Core imports"

# 2. Testar configuração
echo -e "\n${BLUE}[2/15] Testando configuração...${NC}"
python3 -c "
from core.config import Config
c = Config()
assert c.validate_config() == True
print('Config OK')
"
check "Configuração"

# 3. Testar autorização
echo -e "\n${BLUE}[3/15] Testando autorização...${NC}"
python3 -c "
from core.authorization import AuthorizationManager
auth = AuthorizationManager()
auth.add_authorization('127.0.0.1', ['recon'], 'Test', 1)
assert auth.check_authorization('127.0.0.1', 'recon') == True
print('Authorization OK')
"
check "Autorização"

# 4. Testar servidor vulnerável
echo -e "\n${BLUE}[4/15] Testando servidor vulnerável...${NC}"
curl -s http://127.0.0.1:8080/ > /dev/null
check "Servidor vulnerável"

# 5. Testar reconhecimento
echo -e "\n${BLUE}[5/15] Testando reconhecimento...${NC}"
python cli/main.py recon --target 127.0.0.1 --options '{"port_scan": false}' > /dev/null 2>&1
check "Reconhecimento"

# 6. Testar scanner
echo -e "\n${BLUE}[6/15] Testando scanner...${NC}"
python cli/main.py scan --target 127.0.0.1:8080 --type quick > /dev/null 2>&1
check "Scanner"

# 7. Testar exploits
echo -e "\n${BLUE}[7/15] Testando exploits...${NC}"
python cli/main.py exploit --target 127.0.0.1:8080 --name command_injection > /dev/null 2>&1
check "Exploits"

# 8. Testar hash cracking
echo -e "\n${BLUE}[8/15] Testando hash cracking...${NC}"
python cli/main.py crack --hash 0192023a7bbd73250516f069df18b500 --type md5 > /dev/null 2>&1
check "Hash cracking"

# 9. Testar forensics
echo -e "\n${BLUE}[9/15] Testando forensics...${NC}"
echo "test" > /tmp/test.txt
python cli/main.py forensics --file /tmp/test.txt --type hash > /dev/null 2>&1
check "Forensics"

# 10. Testar relatórios
echo -e "\n${BLUE}[10/15] Testando relatórios...${NC}"
python cli/main.py report --format json > /dev/null 2>&1
check "Relatórios JSON"

python cli/main.py report --format html > /dev/null 2>&1
check "Relatórios HTML"

# 11. Testar API
echo -e "\n${BLUE}[11/15] Testando API...${NC}"
python3 -m uvicorn api.server:app --host 127.0.0.1 --port 8000 &
API_PID=$!
sleep 3
curl -s http://127.0.0.1:8000/status > /dev/null
check "API status"
kill $API_PID 2>/dev/null

# 12. Testar modo interativo
echo -e "\n${BLUE}[12/15] Testando modo interativo...${NC}"
echo "exit" | python cli/interactive.py > /dev/null 2>&1
check "Modo interativo"

# 13. Testar web dashboard
echo -e "\n${BLUE}[13/15] Testando web dashboard...${NC}"
python3 web_server.py &
WEB_PID=$!
sleep 3
curl -s http://127.0.0.1:8888/ > /dev/null
check "Web dashboard"
kill $WEB_PID 2>/dev/null

# 14. Testar agentes
echo -e "\n${BLUE}[14/15] Testando agentes...${NC}"
python3 -c "
from agents.crawler.web_crawler import WebCrawlerAgent
from agents.osint.osint_agent import OSINTAgent
from agents.monitor.threat_monitor import ThreatMonitorAgent
print('Agents OK')
"
check "Agentes"

# 15. Testar laboratório
echo -e "\n${BLUE}[15/15] Testando laboratório...${NC}"
ls lab/data/wordlists 2>/dev/null || ls lab/data/*.txt > /dev/null 2>&1
check "Laboratório"

# Resumo final
echo -e "\n========================================="
echo -e "${GREEN}Testes passaram: $PASS${NC}"
echo -e "${RED}Testes falharam: $FAIL${NC}"
echo -e "========================================="

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}TODOS OS TESTES PASSARAM!${NC}"
else
    echo -e "${YELLOW}Alguns testes falharam. Verifique os erros acima.${NC}"
fi
