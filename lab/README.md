# ByteBreaker Test Laboratory

## Descrição
Laboratório de testes seguro para o ByteBreaker Framework.

## Serviços Disponíveis

### 1. Servidor Web Vulnerável
- **URL**: http://127.0.0.1:8080
- **Vulnerabilidades**:
  - XSS em /search
  - SQL Injection em /user
  - Path Traversal em /file
  - Directory listing em /admin
  - Arquivo sensível em /config

### 2. Arquivos de Teste
- `data/forensics_test.txt` - Para análise forense
- `data/test_hash.txt` - Hash para cracking
- `data/secret.txt` - Arquivo com dados sensíveis

## Como Usar

### Iniciar Laboratório
```bash
./lab/start_lab.sh
Executar Testes
bash

./lab/run_tests.sh

Testes Manuais
bash

# Ativar ambiente
source venv/bin/activate

# Testar scan web
python cli/main.py authorize --target 127.0.0.1 --scope recon,scan --by "Test"
python cli/main.py scan --target 127.0.0.1 --type web

# Testar forensics
python cli/main.py forensics --file lab/data/forensics_test.txt --type full

# Testar hash cracking
python cli/main.py crack --hash 0192023a7bbd73250516f069df18b500 --type md5

Aviso

Este laboratório é para uso educacional e testes controlados apenas.
Todos os alvos são locais (127.0.0.1) e não afetam sistemas externos.
