"""
ForensicKit - Digital Forensics Analysis Module
"""
from typing import Dict, Any, Optional, List
import asyncio
import hashlib
import os
import json
from datetime import datetime
from pathlib import Path
import struct

# Try to import magic, but handle if not available
try:
    import magic
    MAGIC_AVAILABLE = True
except ImportError:
    MAGIC_AVAILABLE = False
    print("Warning: python-magic not installed. Using basic file type detection.")


class ForensicKit:
    """Digital forensics analysis module"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.file_types = {
            "application/pdf": "PDF Document",
            "application/zip": "ZIP Archive",
            "application/x-executable": "Executable",
            "image/jpeg": "JPEG Image",
            "image/png": "PNG Image",
            "text/plain": "Text File",
            "application/json": "JSON File",
            "application/xml": "XML File"
        }
    
    async def analyze(self, file_path: str, analysis_type: str = "full") -> Dict[str, Any]:
        """Perform forensic analysis on file"""
        
        if not Path(file_path).exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        results = {
            "file_path": file_path,
            "file_name": Path(file_path).name,
            "file_size": os.path.getsize(file_path),
            "analysis_type": analysis_type,
            "analyzed_at": datetime.now().isoformat()
        }
        
        try:
            if analysis_type in ["full", "hash"]:
                results["hashes"] = await self._calculate_hashes(file_path)
            
            if analysis_type in ["full", "metadata"]:
                results["metadata"] = await self._extract_metadata(file_path)
            
            if analysis_type in ["full", "strings"]:
                results["strings"] = await self._extract_strings(file_path)
            
            if analysis_type == "full":
                results["file_type"] = await self._identify_file_type(file_path)
                results["suspicious_indicators"] = await self._check_suspicious(file_path)
            
            return results
            
        except Exception as e:
            self.logger.error(f"Forensic analysis failed: {e}")
            raise
    
    async def _calculate_hashes(self, file_path: str) -> Dict[str, str]:
        """Calculate file hashes"""
        hashes = {}
        
        hash_functions = {
            "md5": hashlib.md5(),
            "sha1": hashlib.sha1(),
            "sha256": hashlib.sha256()
        }
        
        try:
            with open(file_path, 'rb') as f:
                while chunk := f.read(8192):
                    for hash_func in hash_functions.values():
                        hash_func.update(chunk)
            
            for name, hash_func in hash_functions.items():
                hashes[name] = hash_func.hexdigest()
                
        except Exception as e:
            self.logger.error(f"Hash calculation failed: {e}")
            hashes["error"] = str(e)
        
        return hashes
    
    async def _extract_metadata(self, file_path: str) -> Dict[str, Any]:
        """Extract file metadata"""
        metadata = {}
        file_stat = os.stat(file_path)
        
        metadata["created"] = datetime.fromtimestamp(file_stat.st_ctime).isoformat()
        metadata["modified"] = datetime.fromtimestamp(file_stat.st_mtime).isoformat()
        metadata["accessed"] = datetime.fromtimestamp(file_stat.st_atime).isoformat()
        metadata["permissions"] = oct(file_stat.st_mode)[-3:]
        metadata["size_bytes"] = file_stat.st_size
        
        # Try to identify file type
        if MAGIC_AVAILABLE:
            try:
                file_type = magic.from_file(file_path, mime=True)
                metadata["mime_type"] = file_type
            except:
                pass
        
        return metadata
    
    async def _extract_strings(self, file_path: str, min_length: int = 4) -> List[str]:
        """Extract readable strings from file"""
        strings = []
        
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
                
                # Extract ASCII strings
                current_string = ""
                for byte in content:
                    if 32 <= byte <= 126:  # Printable ASCII
                        current_string += chr(byte)
                    else:
                        if len(current_string) >= min_length:
                            strings.append(current_string)
                        current_string = ""
                
                if len(current_string) >= min_length:
                    strings.append(current_string)
                
                # Limit strings to first 100
                strings = strings[:100]
                
        except Exception as e:
            self.logger.error(f"String extraction failed: {e}")
        
        return strings
    
    async def _identify_file_type(self, file_path: str) -> Dict[str, str]:
        """Identify file type"""
        try:
            if MAGIC_AVAILABLE:
                mime_type = magic.from_file(file_path, mime=True)
                description = magic.from_file(file_path)
                
                return {
                    "mime_type": mime_type,
                    "description": description,
                    "category": self.file_types.get(mime_type, "Unknown")
                }
            else:
                # Basic file type detection by extension
                extension = Path(file_path).suffix.lower()
                ext_types = {
                    ".pdf": "PDF Document",
                    ".zip": "ZIP Archive",
                    ".exe": "Executable",
                    ".jpg": "JPEG Image",
                    ".jpeg": "JPEG Image",
                    ".png": "PNG Image",
                    ".txt": "Text File",
                    ".json": "JSON File",
                    ".xml": "XML File"
                }
                
                return {
                    "mime_type": "unknown",
                    "description": ext_types.get(extension, "Unknown file type"),
                    "category": ext_types.get(extension, "Unknown")
                }
        except Exception as e:
            self.logger.error(f"File type identification failed: {e}")
            return {"error": str(e)}
    
    async def _check_suspicious(self, file_path: str) -> List[Dict[str, str]]:
        """Check for suspicious indicators"""
        indicators = []
        
        try:
            # Check file permissions
            if os.access(file_path, os.X_OK):
                indicators.append({
                    "type": "permissions",
                    "severity": "medium",
                    "description": "File is executable"
                })
            
            # Check for suspicious strings
            strings = await self._extract_strings(file_path)
            suspicious_patterns = [
                "cmd.exe", "powershell", "bash", "sh -c",
                "eval(", "exec(", "system(",
                "base64_decode", "gzinflate",
                "CreateProcess", "ShellExecute",
                "socket", "connect", "bind"
            ]
            
            for string in strings:
                for pattern in suspicious_patterns:
                    if pattern.lower() in string.lower():
                        indicators.append({
                            "type": "suspicious_string",
                            "severity": "high",
                            "description": f"Found suspicious string: {string[:50]}",
                            "pattern": pattern
                        })
                        break
            
            # Check file size
            file_size = os.path.getsize(file_path)
            if file_size > 10 * 1024 * 1024:  # > 10MB
                indicators.append({
                    "type": "file_size",
                    "severity": "low",
                    "description": f"Large file: {file_size} bytes"
                })
            
        except Exception as e:
            self.logger.error(f"Suspicious check failed: {e}")
        
        return indicators
