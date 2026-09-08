"""
VulnScan - Vulnerability Scanner Module
"""
from typing import Dict, Any, List, Optional
import asyncio
import aiohttp
import re
from datetime import datetime
from urllib.parse import urljoin, urlparse
import json


class VulnScan:
    """Automated vulnerability scanner"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.session = None
        self.vulnerabilities = []
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session"""
        if not self.session or self.session.closed:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=30),
                headers={"User-Agent": self.config.scanner.user_agent}
            )
        return self.session
    
    def _normalize_url(self, target: str, port: int = None) -> str:
        """Normalize URL with port"""
        if target.startswith(('http://', 'https://')):
            return target
        elif ':' in target and not target.startswith(('http://', 'https://')):
            # Check if it's IP:port or host:port
            parts = target.split(':')
            if len(parts) == 2 and parts[1].isdigit():
                host = parts[0]
                port = int(parts[1])
                return f"http://{host}:{port}"
        
        if port:
            return f"http://{target}:{port}"
        return f"http://{target}"
    
    async def scan(self, target: str, scan_type: str = "full") -> Dict[str, Any]:
        """Run vulnerability scan"""
        self.vulnerabilities = []
        
        # Extract port if provided
        port = None
        if ':' in target and not target.startswith(('http://', 'https://')):
            parts = target.split(':')
            if len(parts) == 2 and parts[1].isdigit():
                port = int(parts[1])
                target = parts[0]
        
        # Normalize URL
        base_url = self._normalize_url(target, port)
        
        try:
            if scan_type in ["full", "web"]:
                await self._scan_web_vulnerabilities(base_url)
            
            if scan_type in ["full", "network"]:
                await self._scan_network_vulnerabilities(target)
            
            if scan_type == "quick":
                await self._quick_scan(base_url)
            
            return {
                "target": target,
                "url": base_url,
                "scan_type": scan_type,
                "vulnerabilities": self.vulnerabilities,
                "total_found": len(self.vulnerabilities),
                "scan_time": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Vulnerability scan failed: {e}")
            raise
        finally:
            if self.session and not self.session.closed:
                await self.session.close()
    
    async def _quick_scan(self, base_url: str) -> None:
        """Quick scan for common vulnerabilities"""
        # Check for common security headers
        await self._check_security_headers(base_url)
        
        # Check for common files
        await self._check_common_files(base_url)
    
    async def _scan_web_vulnerabilities(self, base_url: str) -> None:
        """Scan for web vulnerabilities"""
        session = await self._get_session()
        
        # Test for SQL Injection
        await self._test_sql_injection(base_url, session)
        
        # Test for XSS
        await self._test_xss(base_url, session)
        
        # Check security headers
        await self._check_security_headers(base_url)
        
        # Check for common files
        await self._check_common_files(base_url)
        
        # Check for directory listing
        await self._check_directory_listing(base_url, session)
    
    async def _scan_network_vulnerabilities(self, target: str) -> None:
        """Scan for network vulnerabilities"""
        # Check for open ports that might indicate vulnerabilities
        common_vulnerable_ports = {
            21: "FTP - Potential anonymous access",
            23: "Telnet - Unencrypted protocol",
            445: "SMB - Potential EternalBlue vulnerability",
            3306: "MySQL - Potential weak authentication",
            5432: "PostgreSQL - Check for weak credentials"
        }
        
        # Basic port check
        import socket
        for port, description in common_vulnerable_ports.items():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex((target, port))
                if result == 0:
                    self.vulnerabilities.append({
                        "type": "network",
                        "severity": "medium",
                        "title": description,
                        "port": port,
                        "target": target
                    })
                sock.close()
            except Exception:
                continue
    
    async def _test_sql_injection(self, base_url: str, session: aiohttp.ClientSession) -> None:
        """Test for SQL injection vulnerabilities"""
        sql_payloads = [
            "'",
            "''",
            "' OR '1'='1",
            "' OR '1'='1' --",
            "' UNION SELECT NULL--",
            "'; DROP TABLE users--",
            "' AND 1=1--",
            "' AND 1=2--"
        ]
        
        test_urls = await self._discover_urls(base_url, session)
        
        for url in test_urls:
            for payload in sql_payloads:
                try:
                    # Test GET parameters
                    if '?' in url:
                        test_url = f"{url}{payload}"
                        async with session.get(test_url) as response:
                            text = await response.text()
                            if self._check_sql_error(text) or "SQL injection detected" in text:
                                self.vulnerabilities.append({
                                    "type": "sql_injection",
                                    "severity": "critical",
                                    "title": "SQL Injection vulnerability",
                                    "url": url,
                                    "payload": payload
                                })
                                break
                except Exception:
                    continue
    
    async def _test_xss(self, base_url: str, session: aiohttp.ClientSession) -> None:
        """Test for XSS vulnerabilities"""
        xss_payloads = [
            "<script>alert(1)</script>",
            "<img src=x onerror=alert(1)>",
            "'><script>alert(1)</script>",
            "\"><script>alert(1)</script>",
            "javascript:alert(1)"
        ]
        
        test_urls = await self._discover_urls(base_url, session)
        
        for url in test_urls:
            for payload in xss_payloads:
                try:
                    if '?' in url:
                        test_url = f"{url}{payload}"
                    else:
                        # Test XSS in search parameter
                        test_url = f"{url}?q={payload}"
                    
                    async with session.get(test_url) as response:
                        text = await response.text()
                        if payload in text:
                            self.vulnerabilities.append({
                                "type": "xss",
                                "severity": "high",
                                "title": "XSS vulnerability",
                                "url": url,
                                "payload": payload
                            })
                            break
                except Exception:
                    continue
    
    async def _check_security_headers(self, base_url: str) -> None:
        """Check for missing security headers"""
        session = await self._get_session()
        
        security_headers = {
            "X-Frame-Options": "Clickjacking protection",
            "X-XSS-Protection": "XSS protection",
            "X-Content-Type-Options": "MIME type sniffing protection",
            "Content-Security-Policy": "Content Security Policy",
            "Strict-Transport-Security": "HSTS",
            "Referrer-Policy": "Referrer policy"
        }
        
        try:
            async with session.get(base_url) as response:
                for header, description in security_headers.items():
                    if header not in response.headers:
                        self.vulnerabilities.append({
                            "type": "missing_header",
                            "severity": "low",
                            "title": f"Missing {header}",
                            "description": description,
                            "url": base_url
                        })
        except Exception as e:
            self.logger.error(f"Security header check failed: {e}")
    
    async def _check_common_files(self, base_url: str) -> None:
        """Check for common sensitive files"""
        session = await self._get_session()
        
        common_files = [
            "robots.txt",
            "sitemap.xml",
            ".git/config",
            ".env",
            "backup.zip",
            "admin/",
            "phpinfo.php",
            "wp-config.php",
            "config.php",
            "database.sql",
            "config"
        ]
        
        for file_path in common_files:
            try:
                url = urljoin(base_url.rstrip('/') + '/', file_path)
                async with session.get(url) as response:
                    if response.status == 200:
                        self.vulnerabilities.append({
                            "type": "sensitive_file",
                            "severity": "high",
                            "title": f"Sensitive file found: {file_path}",
                            "url": url,
                            "status_code": response.status
                        })
            except Exception:
                continue
    
    async def _check_directory_listing(self, base_url: str, session: aiohttp.ClientSession) -> None:
        """Check for directory listing"""
        try:
            async with session.get(base_url) as response:
                text = await response.text()
                if "Index of /" in text or "Directory listing" in text:
                    self.vulnerabilities.append({
                        "type": "directory_listing",
                        "severity": "medium",
                        "title": "Directory listing enabled",
                        "url": base_url
                    })
        except Exception:
            pass
    
    async def _discover_urls(self, base_url: str, session: aiohttp.ClientSession) -> List[str]:
        """Discover URLs from target"""
        urls = []
        
        try:
            async with session.get(base_url) as response:
                if response.status == 200:
                    text = await response.text()
                    # Extract URLs from HTML
                    urls.extend(re.findall(r'href=["\'](.*?)["\']', text))
                    urls.extend(re.findall(r'src=["\'](.*?)["\']', text))
                    
                    # Filter and normalize URLs
                    normalized_urls = []
                    for url in urls:
                        if url.startswith('http'):
                            normalized_urls.append(url)
                        elif url.startswith('/'):
                            normalized_urls.append(urljoin(base_url, url))
                        elif not url.startswith('#') and not url.startswith('javascript:'):
                            normalized_urls.append(urljoin(base_url + '/', url))
                    
                    # Add common test URLs
                    common_paths = ["/search?q=test", "/user?id=1", "/file?name=test.txt"]
                    for path in common_paths:
                        normalized_urls.append(urljoin(base_url + '/', path.lstrip('/')))
                    
                    return list(set(normalized_urls))[:15]  # Limit URLs for testing
        except Exception:
            pass
        
        return [base_url]  # Return base URL if no others found
    
    def _check_sql_error(self, text: str) -> bool:
        """Check for SQL error messages"""
        sql_errors = [
            "SQL syntax",
            "mysql_fetch",
            "ORA-",
            "PostgreSQL",
            "SQLite",
            "Microsoft SQL",
            "ODBC",
            "syntax error",
            "unexpected token",
            "unclosed quotation mark",
            "SQL injection detected"
        ]
        
        text_lower = text.lower()
        return any(error.lower() in text_lower for error in sql_errors)
