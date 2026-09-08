"""
OSINT Agent for ByteBreaker
"""
import asyncio
import aiohttp
from typing import Dict, Any, List, Optional
import json
from datetime import datetime

class OSINTAgent:
    """Open Source Intelligence Agent"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.session = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create session"""
        if not self.session or self.session.closed:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=30),
                headers={"User-Agent": "ByteBreaker-OSINT/1.0"}
            )
        return self.session
    
    async def search_domain(self, domain: str) -> Dict[str, Any]:
        """Search for domain information"""
        results = {
            "domain": domain,
            "dns_records": await self._get_dns_records(domain),
            "whois": await self._get_whois(domain),
            "subdomains": await self._find_subdomains(domain),
            "technologies": await self._detect_technologies(domain),
            "timestamp": datetime.now().isoformat()
        }
        return results
    
    async def search_ip(self, ip: str) -> Dict[str, Any]:
        """Search for IP information"""
        results = {
            "ip": ip,
            "geolocation": await self._get_geolocation(ip),
            "reputation": await self._check_reputation(ip),
            "open_ports": await self._scan_ports(ip),
            "timestamp": datetime.now().isoformat()
        }
        return results
    
    async def _get_dns_records(self, domain: str) -> Dict[str, Any]:
        """Get DNS records"""
        try:
            import dns.resolver
            records = {}
            
            for record_type in ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA']:
                try:
                    answers = dns.resolver.resolve(domain, record_type)
                    records[record_type] = [str(answer) for answer in answers]
                except:
                    records[record_type] = []
            
            return records
        except Exception as e:
            return {"error": str(e)}
    
    async def _get_whois(self, domain: str) -> Dict[str, Any]:
        """Get WHOIS information"""
        try:
            import whois
            w = whois.whois(domain)
            return {
                "registrar": w.registrar,
                "creation_date": str(w.creation_date),
                "expiration_date": str(w.expiration_date),
                "name_servers": w.name_servers
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def _find_subdomains(self, domain: str) -> List[str]:
        """Find subdomains using certificate transparency"""
        subdomains = []
        
        try:
            session = await self._get_session()
            url = f"https://crt.sh/?q=%25.{domain}&output=json"
            
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    for entry in data:
                        name = entry.get('name_value', '')
                        for subdomain in name.split('\n'):
                            if '*' not in subdomain:
                                subdomains.append(subdomain)
        
        except Exception as e:
            self.logger.error(f"Subdomain search failed: {e}")
        
        return list(set(subdomains))
    
    async def _detect_technologies(self, domain: str) -> List[str]:
        """Detect technologies used by website"""
        technologies = []
        
        try:
            session = await self._get_session()
            url = f"https://{domain}"
            
            async with session.get(url) as response:
                headers = response.headers
                
                # Check common technology headers
                tech_headers = {
                    'X-Powered-By': 'Framework',
                    'Server': 'Web Server',
                    'X-AspNet-Version': '.NET',
                    'X-Drupal-Cache': 'Drupal',
                    'X-Generator': 'Generator'
                }
                
                for header, tech_type in tech_headers.items():
                    if header in headers:
                        technologies.append(f"{tech_type}: {headers[header]}")
        
        except Exception as e:
            self.logger.error(f"Technology detection failed: {e}")
        
        return technologies
    
    async def _get_geolocation(self, ip: str) -> Dict[str, Any]:
        """Get IP geolocation"""
        try:
            session = await self._get_session()
            url = f"http://ip-api.com/json/{ip}"
            
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
        except Exception as e:
            return {"error": str(e)}
        
        return {}
    
    async def _check_reputation(self, ip: str) -> Dict[str, Any]:
        """Check IP reputation"""
        # Simulated reputation check
        return {
            "reputation": "unknown",
            "threat_level": "low",
            "source": "simulated"
        }
    
    async def _scan_ports(self, ip: str) -> List[int]:
        """Scan common ports"""
        common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 5432, 8080]
        open_ports = []
        
        for port in common_ports:
            try:
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(ip, port),
                    timeout=2
                )
                writer.close()
                await writer.wait_closed()
                open_ports.append(port)
            except:
                continue
        
        return open_ports
