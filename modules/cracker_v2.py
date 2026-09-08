"""
Enhanced HashCrack with more features
"""
import hashlib
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path
import itertools
import string

class EnhancedHashCrack:
    """Enhanced hash cracking with brute force"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.common_passwords = []
    
    async def brute_force(self, hash_value: str, hash_type: str, 
                         max_length: int = 4, charset: str = string.ascii_lowercase) -> Dict[str, Any]:
        """Brute force hash"""
        start_time = datetime.now()
        attempts = 0
        
        for length in range(1, max_length + 1):
            for password_tuple in itertools.product(charset, repeat=length):
                password = ''.join(password_tuple)
                attempts += 1
                
                calculated = self._calculate_hash(password, hash_type)
                if calculated and calculated.lower() == hash_value.lower():
                    return {
                        "success": True,
                        "password": password,
                        "attempts": attempts,
                        "time_taken": str(datetime.now() - start_time)
                    }
                
                if attempts > self.config.cracker.max_attempts:
                    return {
                        "success": False,
                        "attempts": attempts,
                        "message": "Max attempts reached"
                    }
        
        return {
            "success": False,
            "attempts": attempts,
            "message": "Password not found in search space"
        }
    
    async def hybrid_attack(self, hash_value: str, hash_type: str, 
                          base_words: List[str], append_chars: str = "123!@#") -> Dict[str, Any]:
        """Hybrid attack - wordlist + mutations"""
        start_time = datetime.now()
        attempts = 0
        
        for word in base_words:
            # Try original word
            attempts += 1
            if self._check_hash(word, hash_value, hash_type):
                return {"success": True, "password": word, "attempts": attempts}
            
            # Try with appended characters
            for char in append_chars:
                attempts += 1
                candidate = word + char
                if self._check_hash(candidate, hash_value, hash_type):
                    return {"success": True, "password": candidate, "attempts": attempts}
            
            # Try with common mutations
            mutations = [
                word.capitalize(),
                word.upper(),
                word.replace('a', '@'),
                word.replace('e', '3'),
                word.replace('i', '1'),
                word.replace('o', '0')
            ]
            
            for mutation in mutations:
                attempts += 1
                if self._check_hash(mutation, hash_value, hash_type):
                    return {"success": True, "password": mutation, "attempts": attempts}
        
        return {"success": False, "attempts": attempts}
    
    def _check_hash(self, password: str, hash_value: str, hash_type: str) -> bool:
        """Check if password matches hash"""
        calculated = self._calculate_hash(password, hash_type)
        return calculated and calculated.lower() == hash_value.lower()
    
    def _calculate_hash(self, password: str, hash_type: str) -> Optional[str]:
        """Calculate hash"""
        try:
            if hash_type == "md5":
                return hashlib.md5(password.encode()).hexdigest()
            elif hash_type == "sha1":
                return hashlib.sha1(password.encode()).hexdigest()
            elif hash_type == "sha256":
                return hashlib.sha256(password.encode()).hexdigest()
            elif hash_type == "sha512":
                return hashlib.sha512(password.encode()).hexdigest()
            else:
                return None
        except:
            return None
