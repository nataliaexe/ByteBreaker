"""
Threat Monitor Agent for ByteBreaker
"""
import asyncio
import aiohttp
from typing import Dict, Any, List, Optional
import json
from datetime import datetime, timedelta

class ThreatMonitorAgent:
    """Autonomous threat monitoring agent"""
    
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.session = None
        self.threat_feeds = []
        self.monitored_targets = []
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create session"""
        if not self.session or self.session.closed:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=30),
                headers={"User-Agent": "ByteBreaker-Monitor/1.0"}
            )
        return self.session
    
    async def monitor_target(self, target: str, interval_minutes: int = 60) -> None:
        """Monitor target for changes"""
        self.monitored_targets.append({
            "target": target,
            "interval": interval_minutes,
            "last_check": None,
            "status": "monitoring"
        })
        
        self.logger.info(f"Started monitoring {target}")
        
        while True:
            try:
                check_result = await self.check_target(target)
                self.logger.info(f"Monitor check completed for {target}")
                
                # Store result
                self.threat_feeds.append({
                    "target": target,
                    "timestamp": datetime.now().isoformat(),
                    "result": check_result
                })
                
                # Wait for next check
                await asyncio.sleep(interval_minutes * 60)
            
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Monitor check failed for {target}: {e}")
                await asyncio.sleep(60)  # Retry in 1 minute
    
    async def check_target(self, target: str) -> Dict[str, Any]:
        """Check target for changes/threats"""
        session = await self._get_session()
        
        result = {
            "target": target,
            "status": "unknown",
            "response_time": None,
            "security_headers": {},
            "threats_found": []
        }
        
        try:
            url = f"http://{target}" if not target.startswith(('http://', 'https://')) else target
            
            start_time = datetime.now()
            async with session.get(url) as response:
                response_time = (datetime.now() - start_time).total_seconds()
                
                result["status"] = "up" if response.status < 400 else "down"
                result["response_time"] = response_time
                result["status_code"] = response.status
                
                # Check security headers
                security_headers = {
                    "X-Frame-Options": "Clickjacking protection",
                    "X-XSS-Protection": "XSS protection",
                    "Content-Security-Policy": "CSP",
                    "Strict-Transport-Security": "HSTS"
                }
                
                for header, description in security_headers.items():
                    result["security_headers"][header] = header in response.headers
                    
                    if header not in response.headers:
                        result["threats_found"].append({
                            "type": "missing_header",
                            "severity": "low",
                            "description": f"Missing {description}"
                        })
        
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
        
        return result
    
    def get_monitoring_status(self) -> Dict[str, Any]:
        """Get monitoring status"""
        return {
            "monitored_targets": self.monitored_targets,
            "threat_feed_count": len(self.threat_feeds),
            "recent_threats": self.threat_feeds[-10:] if self.threat_feeds else []
        }
    
    def generate_alert(self, threat: Dict[str, Any]) -> Dict[str, Any]:
        """Generate alert for threat"""
        return {
            "alert": True,
            "severity": threat.get("severity", "medium"),
            "message": threat.get("description", "Unknown threat"),
            "timestamp": datetime.now().isoformat(),
            "action_required": threat.get("severity") in ["high", "critical"]
        }
