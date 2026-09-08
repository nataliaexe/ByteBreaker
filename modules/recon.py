"""
ReconX - Advanced reconnaissance module
"""
from typing import Dict, Any, List, Optional
import asyncio
import socket
import ipaddress
import ssl
from datetime import datetime
import json
import dns.resolver
import whois


class ReconX:
    """Advanced reconnaissance module"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.results = {}
    
    async def scan(self, target: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """Perform reconnaissance scan"""
        options = options or {}
        
        tasks = []
        task_names = []
        
        # Basic info gathering
        tasks.append(self.get_basic_info(target))
        task_names.append("basic_info")
        
        # DNS enumeration if domain
        if not self._is_ip(target):
            tasks.append(self.dns_enumeration(target))
            task_names.append("dns_enum")
            
            tasks.append(self.get_whois_info(target))
            task_names.append("whois")
        
        # Port scanning if requested
        if options.get("port_scan", True):
            tasks.append(self.port_scan(target, options.get("ports", "common")))
            task_names.append("ports")
        
        # SSL analysis if requested
        if options.get("ssl_check", True):
            tasks.append(self.ssl_analysis(target))
            task_names.append("ssl")
        
        # Run all tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        processed_results = {}
        
        for name, result in zip(task_names, results):
            if isinstance(result, Exception):
                self.logger.error(f"Task {name} failed: {result}")
                processed_results[name] = {"error": str(result)}
            else:
                processed_results[name] = result
        
        return processed_results
    
    async def get_basic_info(self, target: str) -> Dict[str, Any]:
        """Get basic information about target"""
        try:
            ip_addresses = []
            
            if self._is_ip(target):
                ip_addresses.append(target)
            else:
                # Resolve domain to IPs
                ips = socket.getaddrinfo(target, None)
                ip_addresses = list(set([ip[4][0] for ip in ips]))
            
            return {
                "target": target,
                "ip_addresses": ip_addresses,
                "is_ip": self._is_ip(target),
                "resolved_at": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Basic info failed: {e}")
            raise
    
    async def dns_enumeration(self, domain: str) -> Dict[str, Any]:
        """Enumerate DNS records"""
        records = {}
        
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME']
        
        for record_type in record_types:
            try:
                answers = dns.resolver.resolve(domain, record_type)
                records[record_type] = [str(answer) for answer in answers]
            except dns.resolver.NoAnswer:
                records[record_type] = []
            except dns.resolver.NXDOMAIN:
                records[record_type] = []
                break
            except Exception as e:
                records[record_type] = [f"Error: {e}"]
        
        return records
    
    async def get_whois_info(self, domain: str) -> Dict[str, Any]:
        """Get WHOIS information"""
        try:
            w = whois.whois(domain)
            return {
                "registrar": w.registrar,
                "creation_date": str(w.creation_date),
                "expiration_date": str(w.expiration_date),
                "name_servers": w.name_servers,
                "status": w.status
            }
        except Exception as e:
            self.logger.error(f"WHOIS lookup failed: {e}")
            return {"error": str(e)}
    
    async def port_scan(self, target: str, port_type: str = "common") -> Dict[str, Any]:
        """Scan ports on target"""
        common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 
                       993, 995, 1723, 3306, 3389, 5432, 5900, 8080, 8443]
        
        if port_type == "common":
            ports = common_ports
        elif port_type == "full":
            ports = range(1, 65536)
        elif port_type == "top100":
            ports = common_ports[:100]
        else:
            ports = common_ports
        
        open_ports = []
        
        # Create tasks for concurrent scanning
        tasks = []
        for port in ports:
            tasks.append(self._check_port(target, port))
        
        results = await asyncio.gather(*tasks)
        
        for port, is_open in zip(ports, results):
            if is_open:
                service = await self._identify_service(target, port)
                open_ports.append({
                    "port": port,
                    "service": service,
                    "status": "open"
                })
        
        return {
            "total_scanned": len(ports),
            "open_ports": open_ports,
            "scan_time": datetime.now().isoformat()
        }
    
    async def _check_port(self, target: str, port: int) -> bool:
        """Check if port is open"""
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(target, port),
                timeout=self.config.scanner.timeout
            )
            writer.close()
            await writer.wait_closed()
            return True
        except:
            return False
    
    async def _identify_service(self, target: str, port: int) -> str:
        """Identify service running on port"""
        service_signatures = {
            21: "FTP",
            22: "SSH",
            23: "Telnet",
            25: "SMTP",
            53: "DNS",
            80: "HTTP",
            110: "POP3",
            143: "IMAP",
            443: "HTTPS",
            445: "SMB",
            3306: "MySQL",
            3389: "RDP",
            5432: "PostgreSQL",
            5900: "VNC",
            8080: "HTTP-Proxy",
            8443: "HTTPS-Alt"
        }
        
        return service_signatures.get(port, "Unknown")
    
    async def ssl_analysis(self, target: str) -> Dict[str, Any]:
        """Analyze SSL/TLS configuration"""
        try:
            context = ssl.create_default_context()
            with socket.create_connection((target, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=target) as ssock:
                    cert = ssock.getpeercert()
                    cipher = ssock.cipher()
                    version = ssock.version()
                    
                    return {
                        "ssl_version": version,
                        "cipher": cipher,
                        "certificate": {
                            "subject": cert.get('subject') if cert else None,
                            "issuer": cert.get('issuer') if cert else None,
                            "notBefore": cert.get('notBefore') if cert else None,
                            "notAfter": cert.get('notAfter') if cert else None
                        }
                    }
        except Exception as e:
            self.logger.error(f"SSL analysis failed: {e}")
            return {"error": str(e)}
    
    def _is_ip(self, target: str) -> bool:
        """Check if target is IP address"""
        try:
            ipaddress.ip_address(target)
            return True
        except ValueError:
            return False
