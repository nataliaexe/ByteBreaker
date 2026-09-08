"""
HashCrack - Password Hash Cracking Module
"""
from typing import Dict, Any, Optional, List
import hashlib
import asyncio
from datetime import datetime
import os
from pathlib import Path


class HashCrack:
    """Password hash cracking module"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.common_passwords = [
            "password", "123456", "123456789", "qwerty", "abc123",
            "admin", "letmein", "welcome", "monkey", "dragon",
            "password1", "12345678", "12345", "iloveyou", "111111",
            "123123", "admin123", "root", "toor", "test",
            "guest", "default", "changeme", "passwd", "secret"
        ]
    
    async def crack(self, hash_value: str, hash_type: str, 
                   wordlist: Optional[str] = None) -> Dict[str, Any]:
        """Attempt to crack hash"""
        
        self.logger.info(f"Starting {hash_type} hash cracking")
        
        start_time = datetime.now()
        attempts = 0
        
        # Validate hash format
        if not self._validate_hash(hash_value, hash_type):
            return {
                "success": False,
                "error": f"Invalid {hash_type} hash format",
                "attempts": 0,
                "time_taken": str(datetime.now() - start_time)
            }
        
        # Use custom wordlist if provided
        if wordlist and Path(wordlist).exists():
            passwords = self._load_wordlist(wordlist)
        else:
            passwords = self.common_passwords
        
        # Try each password
        for password in passwords:
            attempts += 1
            
            # Check if max attempts reached
            if attempts > self.config.cracker.max_attempts:
                break
            
            # Calculate hash
            calculated_hash = self._calculate_hash(password.strip(), hash_type)
            
            if calculated_hash and calculated_hash.lower() == hash_value.lower():
                time_taken = datetime.now() - start_time
                self.logger.info(f"Hash cracked successfully after {attempts} attempts")
                
                return {
                    "success": True,
                    "password": password.strip(),
                    "hash_type": hash_type,
                    "attempts": attempts,
                    "time_taken": str(time_taken),
                    "cracked_at": datetime.now().isoformat()
                }
        
        time_taken = datetime.now() - start_time
        
        return {
            "success": False,
            "hash_type": hash_type,
            "attempts": attempts,
            "time_taken": str(time_taken),
            "message": "Hash not cracked with available wordlist"
        }
    
    def _validate_hash(self, hash_value: str, hash_type: str) -> bool:
        """Validate hash format"""
        hash_lengths = {
            "md5": 32,
            "sha1": 40,
            "sha256": 64
        }
        
        expected_length = hash_lengths.get(hash_type)
        if not expected_length:
            return False
        
        # Check if hex string
        try:
            int(hash_value, 16)
            return len(hash_value) == expected_length
        except ValueError:
            return False
    
    def _calculate_hash(self, password: str, hash_type: str) -> Optional[str]:
        """Calculate hash of password"""
        try:
            if hash_type == "md5":
                return hashlib.md5(password.encode()).hexdigest()
            elif hash_type == "sha1":
                return hashlib.sha1(password.encode()).hexdigest()
            elif hash_type == "sha256":
                return hashlib.sha256(password.encode()).hexdigest()
            else:
                return None
        except Exception as e:
            self.logger.error(f"Hash calculation failed: {e}")
            return None
    
    def _load_wordlist(self, wordlist_path: str) -> List[str]:
        """Load wordlist from file"""
        passwords = []
        try:
            with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                passwords = f.readlines()
            self.logger.info(f"Loaded {len(passwords)} passwords from wordlist")
        except Exception as e:
            self.logger.error(f"Failed to load wordlist: {e}")
        
        return passwords if passwords else self.common_passwords
    
    async def crack_multiple(self, hashes: List[Dict[str, str]], 
                            wordlist: Optional[str] = None) -> List[Dict[str, Any]]:
        """Crack multiple hashes"""
        results = []
        
        for hash_info in hashes:
            hash_value = hash_info.get("hash")
            hash_type = hash_info.get("type", "md5")
            
            if hash_value:
                result = await self.crack(hash_value, hash_type, wordlist)
                result["original_hash"] = hash_value
                results.append(result)
        
        return results
    
    def generate_wordlist(self, base_words: List[str], 
                         mutations: bool = True) -> List[str]:
        """Generate wordlist with mutations"""
        wordlist = set(base_words)
        
        if mutations:
            for word in base_words:
                # Common mutations
                wordlist.add(word.capitalize())
                wordlist.add(word.upper())
                wordlist.add(word.lower())
                wordlist.add(word + "123")
                wordlist.add(word + "!")
                wordlist.add(word + "@123")
                wordlist.add("123" + word)
                wordlist.add(word.replace("a", "@"))
                wordlist.add(word.replace("e", "3"))
                wordlist.add(word.replace("i", "1"))
                wordlist.add(word.replace("o", "0"))
        
        return list(wordlist)
