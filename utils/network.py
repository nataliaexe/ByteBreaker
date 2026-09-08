"""
Network utility functions for ByteBreaker
"""
import socket
import ipaddress
import asyncio
from typing import Optional, List, Tuple
import re


def validate_ip(ip: str) -> bool:
    """Validate IP address"""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def validate_domain(domain: str) -> bool:
    """Validate domain name"""
    pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
    return re.match(pattern, domain) is not None


def resolve_host(hostname: str) -> List[str]:
    """Resolve hostname to IP addresses"""
    try:
        return [ip[4][0] for ip in socket.getaddrinfo(hostname, None)]
    except socket.gaierror:
        return []


def get_service_name(port: int, protocol: str = "tcp") -> str:
    """Get service name for port"""
    try:
        return socket.getservbyport(port, protocol)
    except OSError:
        return "unknown"


def parse_target(target: str) -> Tuple[str, Optional[str]]:
    """Parse target string into host and port"""
    if ":" in target:
        host, port = target.rsplit(":", 1)
        return host, port
    return target, None


def is_port_open(host: str, port: int, timeout: int = 5) -> bool:
    """Check if port is open on host"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except socket.error:
        return False


async def async_check_port(host: str, port: int, timeout: int = 5) -> bool:
    """Asynchronously check if port is open"""
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port),
            timeout=timeout
        )
        writer.close()
        await writer.wait_closed()
        return True
    except:
        return False


def get_ip_range(start_ip: str, end_ip: str) -> List[str]:
    """Get IP addresses in range"""
    start = ipaddress.ip_address(start_ip)
    end = ipaddress.ip_address(end_ip)
    
    if start.version != end.version:
        raise ValueError("IP versions don't match")
    
    ip_range = []
    current = start
    while current <= end:
        ip_range.append(str(current))
        current += 1
    
    return ip_range


def calculate_cidr(ip: str, prefix: int) -> str:
    """Calculate CIDR notation"""
    try:
        network = ipaddress.ip_network(f"{ip}/{prefix}", strict=False)
        return str(network)
    except ValueError:
        return ""


def get_interface_info(interface: str = "eth0") -> dict:
    """Get network interface information"""
    import subprocess
    
    try:
        result = subprocess.run(
            ["ip", "addr", "show", interface],
            capture_output=True,
            text=True,
            check=True
        )
        return {
            "interface": interface,
            "info": result.stdout.strip()
        }
    except subprocess.CalledProcessError:
        return {"error": f"Interface {interface} not found"}
