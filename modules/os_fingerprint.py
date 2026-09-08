"""
OS Fingerprinting Module
"""
import asyncio
from typing import Dict, Any
from datetime import datetime
import socket

class OSFingerprint:
    """OS fingerprinting module"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
    
    async def fingerprint(self, target: str) -> Dict[str, Any]:
        """Fingerprint OS"""
        signatures = {
            "Linux": ["ubuntu", "debian", "centos", "fedora", "kali"],
            "Windows": ["windows", "microsoft", "win32", "win64"],
            "MacOS": ["darwin", "apple", "macos"]
        }
        
        result = {
            "target": target,
            "detected_os": "Unknown",
            "confidence": 0,
            "signatures_found": [],
            "timestamp": datetime.now().isoformat()
        }
        
        # Try TCP window size analysis
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((target, 80))
            
            # Send HTTP request
            sock.send(b"GET / HTTP/1.0\r\n\r\n")
            response = sock.recv(1024).decode('utf-8', errors='ignore')
            
            # Check server header
            for line in response.split('\r\n'):
                if line.lower().startswith('server:'):
                    server = line.split(':', 1)[1].strip()
                    result["signatures_found"].append(f"Server: {server}")
                    
                    # Detect OS from server header
                    for os_name, keywords in signatures.items():
                        for keyword in keywords:
                            if keyword in server.lower():
                                result["detected_os"] = os_name
                                result["confidence"] = 80
            
            sock.close()
            
        except Exception as e:
            self.logger.error(f"Fingerprint failed: {e}")
        
        # Try TTL analysis
        try:
            import subprocess
            ping_result = subprocess.run(
                ["ping", "-c", "1", target],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if "ttl=" in ping_result.stdout.lower():
                ttl_line = [l for l in ping_result.stdout.split('\n') if 'ttl=' in l.lower()]
                if ttl_line:
                    ttl = int(ttl_line[0].split('ttl=')[1].split()[0])
                    result["signatures_found"].append(f"TTL: {ttl}")
                    
                    # TTL-based detection
                    if ttl <= 64:
                        if result["detected_os"] == "Unknown":
                            result["detected_os"] = "Linux/Unix"
                            result["confidence"] = 60
                    elif ttl <= 128:
                        if result["detected_os"] == "Unknown":
                            result["detected_os"] = "Windows"
                            result["confidence"] = 60
        
        except Exception:
            pass
        
        return result
