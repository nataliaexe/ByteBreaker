"""
Enhanced Engine with all features
"""
from typing import Optional, Dict, Any, List
import asyncio
from concurrent.futures import ThreadPoolExecutor
import json
from datetime import datetime
from pathlib import Path

from .config import Config
from .logger import ByteBreakerLogger
from .authorization import AuthorizationManager


class EnhancedEngine:
    """Enhanced engine with all modules"""
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.logger = ByteBreakerLogger()
        self.auth_manager = AuthorizationManager()
        
        self.modules = {}
        self.agents = {}
        self.results = {}
        self.module_errors = {}
        
        self.executor = ThreadPoolExecutor(max_workers=self.config.scanner.max_threads)
        
        self._register_modules()
        self._register_agents()
    
    def _register_modules(self) -> None:
        """Register all modules"""
        module_imports = {
            "recon": ("modules.recon", "ReconX"),
            "scanner": ("modules.scanner", "VulnScan"),
            "exploit": ("modules.exploit", "ExploitLab"),
            "cracker": ("modules.cracker", "HashCrack"),
            "forensics": ("modules.forensics", "ForensicKit"),
            "dir_bruteforce": ("modules.dir_bruteforce", "DirBruteforce"),
            "network_sniffer": ("modules.network_sniffer", "NetworkSniffer"),
            "os_fingerprint": ("modules.os_fingerprint", "OSFingerprint")
        }
        
        import importlib
        
        for module_name, (import_path, class_name) in module_imports.items():
            try:
                module = importlib.import_module(import_path)
                module_class = getattr(module, class_name)
                
                if module_name == "exploit":
                    self.modules[module_name] = module_class(
                        self.config, self.logger, self.auth_manager
                    )
                else:
                    self.modules[module_name] = module_class(
                        self.config, self.logger
                    )
                
                self.logger.info(f"Module loaded: {module_name}")
            except ImportError as e:
                self.module_errors[module_name] = f"Import error: {e}"
            except Exception as e:
                self.module_errors[module_name] = f"Error: {e}"
    
    def _register_agents(self) -> None:
        """Register agents"""
        agent_imports = {
            "crawler": ("agents.crawler.web_crawler", "WebCrawlerAgent"),
            "osint": ("agents.osint.osint_agent", "OSINTAgent"),
            "monitor": ("agents.monitor.threat_monitor", "ThreatMonitorAgent")
        }
        
        import importlib
        
        for agent_name, (import_path, class_name) in agent_imports.items():
            try:
                module = importlib.import_module(import_path)
                agent_class = getattr(module, class_name)
                self.agents[agent_name] = agent_class(self.config, self.logger)
                self.logger.info(f"Agent loaded: {agent_name}")
            except ImportError as e:
                self.logger.warning(f"Agent {agent_name} not available: {e}")
            except Exception as e:
                self.logger.error(f"Failed to load agent {agent_name}: {e}")
    
    async def run_recon(self, target: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """Run reconnaissance"""
        if not self.auth_manager.check_authorization(target, "recon"):
            raise PermissionError(f"No authorization for target: {target}")
        
        if "recon" not in self.modules:
            raise ValueError("Recon module not available")
        
        module = self.modules["recon"]
        results = await module.scan(target, options or {})
        
        self.results["recon"] = {
            "target": target,
            "timestamp": datetime.now().isoformat(),
            "data": results
        }
        
        return results
    
    async def run_scan(self, target: str, scan_type: str = "full") -> Dict[str, Any]:
        """Run vulnerability scan"""
        if not self.auth_manager.check_authorization(target, "scan"):
            raise PermissionError(f"No authorization for target: {target}")
        
        if "scanner" not in self.modules:
            raise ValueError("Scanner module not available")
        
        module = self.modules["scanner"]
        results = await module.scan(target, scan_type)
        
        self.results["scan"] = {
            "target": target,
            "scan_type": scan_type,
            "timestamp": datetime.now().isoformat(),
            "data": results
        }
        
        return results
    
    async def run_exploit(self, target: str, exploit_name: str, payload: Optional[str] = None) -> Dict[str, Any]:
        """Run exploit"""
        if not self.auth_manager.check_authorization(target, "exploit"):
            raise PermissionError(f"No exploit authorization for target: {target}")
        
        if "exploit" not in self.modules:
            raise ValueError("Exploit module not available")
        
        module = self.modules["exploit"]
        results = await module.run(target, exploit_name, payload)
        
        self.results["exploit"] = {
            "target": target,
            "exploit": exploit_name,
            "timestamp": datetime.now().isoformat(),
            "data": results
        }
        
        return results
    
    async def run_cracker(self, hash_value: str, hash_type: str, wordlist: Optional[str] = None) -> Dict[str, Any]:
        """Run hash cracking"""
        if "cracker" not in self.modules:
            raise ValueError("Cracker module not available")
        
        module = self.modules["cracker"]
        results = await module.crack(hash_value, hash_type, wordlist)
        
        self.results["cracker"] = {
            "hash_type": hash_type,
            "timestamp": datetime.now().isoformat(),
            "success": results.get("success", False)
        }
        
        return results
    
    async def run_forensics(self, file_path: str, analysis_type: str = "full") -> Dict[str, Any]:
        """Run forensic analysis"""
        if "forensics" not in self.modules:
            raise ValueError("Forensics module not available")
        
        module = self.modules["forensics"]
        results = await module.analyze(file_path, analysis_type)
        
        self.results["forensics"] = {
            "file": file_path,
            "timestamp": datetime.now().isoformat(),
            "data": results
        }
        
        return results
    
    async def run_dir_bruteforce(self, target: str) -> Dict[str, Any]:
        """Run directory bruteforce"""
        if "dir_bruteforce" not in self.modules:
            raise ValueError("Directory bruteforce module not available")
        
        module = self.modules["dir_bruteforce"]
        results = await module.scan(target)
        
        self.results["dir_bruteforce"] = {
            "target": target,
            "timestamp": datetime.now().isoformat(),
            "data": results
        }
        
        return results
    
    async def run_os_fingerprint(self, target: str) -> Dict[str, Any]:
        """Run OS fingerprinting"""
        if "os_fingerprint" not in self.modules:
            raise ValueError("OS fingerprint module not available")
        
        module = self.modules["os_fingerprint"]
        results = await module.fingerprint(target)
        
        self.results["os_fingerprint"] = {
            "target": target,
            "timestamp": datetime.now().isoformat(),
            "data": results
        }
        
        return results
    
    async def run_network_sniff(self, interface: str = "eth0", count: int = 100) -> Dict[str, Any]:
        """Run network sniffing"""
        if "network_sniffer" not in self.modules:
            raise ValueError("Network sniffer module not available")
        
        module = self.modules["network_sniffer"]
        results = await module.sniff(interface, count)
        
        self.results["network_sniff"] = {
            "interface": interface,
            "timestamp": datetime.now().isoformat(),
            "data": results
        }
        
        return results
    
    def generate_report(self, report_type: str = "json") -> str:
        """Generate report"""
        report_data = {
            "generated_at": datetime.now().isoformat(),
            "results": self.results,
            "modules_available": list(self.modules.keys()),
            "agents_available": list(self.agents.keys()),
            "module_errors": self.module_errors
        }
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if report_type == "json":
            report_path = self.config.reports_dir / f"report_{timestamp}.json"
            with open(report_path, 'w') as f:
                json.dump(report_data, f, indent=4)
            return str(report_path)
        
        elif report_type == "html":
            report_path = self.config.reports_dir / f"report_{timestamp}.html"
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>ByteBreaker Report</title>
                <style>
                    body {{ font-family: Arial; margin: 20px; }}
                    h1 {{ color: #00ff88; }}
                    pre {{ background: #f5f5f5; padding: 10px; }}
                </style>
            </head>
            <body>
                <h1>ByteBreaker Report</h1>
                <p>Generated: {report_data['generated_at']}</p>
                <pre>{json.dumps(report_data, indent=4)}</pre>
            </body>
            </html>
            """
            with open(report_path, 'w') as f:
                f.write(html_content)
            return str(report_path)
        
        return ""
    
    def generate_pdf_report(self) -> str:
        """Generate PDF report"""
        from utils.pdf_report import PDFReportGenerator
        
        generator = PDFReportGenerator(self.config, self.logger)
        report_path = self.config.reports_dir / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        return generator.generate(self.results, str(report_path))
    
    def get_status(self) -> Dict[str, Any]:
        """Get framework status"""
        return {
            "modules_loaded": list(self.modules.keys()),
            "agents_loaded": list(self.agents.keys()),
            "module_errors": self.module_errors,
            "results_count": len(self.results),
            "authorizations": len(self.auth_manager.list_authorizations()),
            "config_valid": self.config.validate_config(),
            "timestamp": datetime.now().isoformat()
        }
    
    def cleanup(self) -> None:
        """Cleanup resources"""
        try:
            self.executor.shutdown(wait=True)
            self.logger.info("Engine shutdown complete")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
