"""
Cryptography utility functions for ByteBreaker
"""
import hashlib
import base64
import os
from typing import Optional, Dict, Any
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2


def calculate_hash(data: bytes, algorithm: str = "sha256") -> str:
    """Calculate hash of data"""
    hash_functions = {
        "md5": hashlib.md5,
        "sha1": hashlib.sha1,
        "sha256": hashlib.sha256,
        "sha512": hashlib.sha512
    }
    
    if algorithm not in hash_functions:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")
    
    hash_func = hash_functions[algorithm]()
    hash_func.update(data)
    return hash_func.hexdigest()


def encode_base64(data: bytes) -> str:
    """Encode data to base64"""
    return base64.b64encode(data).decode('utf-8')


def decode_base64(data: str) -> bytes:
    """Decode base64 data"""
    try:
        return base64.b64decode(data.encode('utf-8'))
    except:
        return b""


def generate_key(password: str, salt: Optional[bytes] = None) -> tuple:
    """Generate encryption key from password"""
    if salt is None:
        salt = os.urandom(16)
    
    kdf = PBKDF2(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key, salt


def encrypt_data(data: bytes, key: bytes) -> bytes:
    """Encrypt data using Fernet"""
    f = Fernet(key)
    return f.encrypt(data)


def decrypt_data(encrypted_data: bytes, key: bytes) -> bytes:
    """Decrypt data using Fernet"""
    f = Fernet(key)
    return f.decrypt(encrypted_data)


def hash_password(password: str, salt: Optional[bytes] = None) -> Dict[str, str]:
    """Hash password with salt"""
    if salt is None:
        salt = os.urandom(16)
    
    # Use PBKDF2 for password hashing
    kdf = PBKDF2(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = kdf.derive(password.encode())
    
    return {
        "hash": base64.b64encode(key).decode('utf-8'),
        "salt": base64.b64encode(salt).decode('utf-8'),
        "algorithm": "PBKDF2-SHA256",
        "iterations": 100000
    }


def verify_password(password: str, password_hash: str, salt: str, 
                   iterations: int = 100000) -> bool:
    """Verify password against hash"""
    try:
        salt_bytes = base64.b64decode(salt.encode('utf-8'))
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt_bytes,
            iterations=iterations,
        )
        key = kdf.derive(password.encode())
        calculated_hash = base64.b64encode(key).decode('utf-8')
        return calculated_hash == password_hash
    except:
        return False
