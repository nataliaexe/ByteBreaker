"""
Directory Bruteforce Module
"""
import asyncio
import aiohttp
from typing import Dict, Any, List
from datetime import datetime

class DirBruteforce:
    """Directory bruteforce module"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.common_paths = [
            "admin", "login", "wp-admin", "administrator",
            "backup", "config", "uploads", "images",
            "css", "js", "api", "test", "dev",
            "robots.txt", "sitemap.xml", ".git", ".env",
            "phpinfo.php", "info.php", "server-status"
        ]
    
    async def scan(self, target: str) -> Dict[str, Any]:
        """Bruteforce directories"""
        session = aiohttp.ClientSession()
        found_paths = []
        
        base_url = f"http://{target}" if not target.startswith(('http://', 'https://')) else target
        
        for path in self.common_paths:
            url = f"{base_url.rstrip('/')}/{path}"
            try:
                async with session.get(url, timeout=5) as response:
                    if response.status in [200, 301, 302, 403]:
                        found_paths.append({
                            "path": path,
                            "status": response.status,
                            "url": url
                        })
                        self.logger.info(f"Found: {path} ({response.status})")
            except:
                continue
        
        await session.close()
        
        return {
            "target": target,
            "found_paths": found_paths,
            "total_found": len(found_paths),
            "scan_time": datetime.now().isoformat()
        }
