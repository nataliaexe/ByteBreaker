"""
Network Sniffer Module
"""
import asyncio
from typing import Dict, Any, List
from datetime import datetime
import struct
import socket

class NetworkSniffer:
    """Network sniffing module"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.packets = []
    
    async def sniff(self, interface: str = "eth0", count: int = 100) -> Dict[str, Any]:
        """Sniff network packets"""
        try:
            import scapy.all as scapy
            
            self.packets = []
            
            def packet_handler(packet):
                if len(self.packets) < count:
                    self.packets.append({
                        "summary": packet.summary(),
                        "src": packet.getlayer(scapy.IP).src if packet.haslayer(scapy.IP) else "N/A",
                        "dst": packet.getlayer(scapy.IP).dst if packet.haslayer(scapy.IP) else "N/A",
                        "proto": packet.getlayer(scapy.IP).proto if packet.haslayer(scapy.IP) else "N/A",
                        "size": len(packet)
                    })
            
            scapy.sniff(iface=interface, prn=packet_handler, count=count, timeout=30)
            
            return {
                "interface": interface,
                "packets_captured": len(self.packets),
                "packets": self.packets,
                "sniff_time": datetime.now().isoformat()
            }
            
        except ImportError:
            self.logger.warning("Scapy not installed, using basic socket sniffing")
            return await self._basic_sniff(interface, count)
    
    async def _basic_sniff(self, interface: str, count: int) -> Dict[str, Any]:
        """Basic sniffing without scapy"""
        return {
            "interface": interface,
            "packets_captured": 0,
            "error": "Scapy not installed. Install with: pip install scapy",
            "sniff_time": datetime.now().isoformat()
        }
