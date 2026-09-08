#!/bin/bash

# Quick test script for ByteBreaker
echo "Running ByteBreaker Quick Tests..."

# Test imports
echo "Testing imports..."
python3 -c "
import sys
sys.path.insert(0, '.')
from core.config import Config
from core.logger import ByteBreakerLogger
from core.authorization import AuthorizationManager
print('Core imports successful')
"

# Test config
echo "Testing configuration..."
python3 -c "
import sys
sys.path.insert(0, '.')
from core.config import Config
config = Config()
print(f'Config valid: {config.validate_config()}')
print(f'Max threads: {config.scanner.max_threads}')
print(f'Timeout: {config.scanner.timeout}')
"

# Test authorization
echo "Testing authorization..."
python3 -c "
import sys
sys.path.insert(0, '.')
from core.authorization import AuthorizationManager
auth = AuthorizationManager('test_auth.json')
auth.add_authorization('127.0.0.1', ['recon'], 'Test', 1)
print(f'Authorized: {auth.check_authorization(\"127.0.0.1\", \"recon\")}')
import os
os.remove('test_auth.json')
"

# Test hash cracking
echo "Testing hash cracking..."
python3 -c "
import sys, asyncio
sys.path.insert(0, '.')
from modules.cracker import HashCrack
from core.config import Config
from core.logger import ByteBreakerLogger
import hashlib

async def test():
    cracker = HashCrack(Config(), ByteBreakerLogger())
    hash_value = hashlib.md5('password'.encode()).hexdigest()
    result = await cracker.crack(hash_value, 'md5')
    print(f'Cracked: {result[\"success\"]}')
    print(f'Password: {result.get(\"password\", \"Not found\")}')

asyncio.run(test())
"

echo "Quick tests complete!"
