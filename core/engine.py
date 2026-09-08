"""
Main engine for ByteBreaker Framework
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


class Engine:
    """Main engine orchestrating all modules"""
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.logger = ByteBreakerLogger()
        self.auth_manager = AuthorizationManager()
        
        # Module registry
        self.modules = {}
        self.results = {}
        
        # Thread pool for parallel operations
        self.executor = ThreadPoolExecutor(max_workers=self.config.scanner.max_threads)
        
        # Initialize modules
        self._register_modules()
    
    def _register_modules(self) -> None:
        """Register all available modules"""
        try:
            from modules.recon import ReconX
            from modules.scanner import VulnScan
            from modules.exploit import ExploitLab
            from modules.cracker import HashCrack
            from modules.forensics import ForensicKit
            
            self.modules = {
                "recon": ReconX(self.config, self.logger),
                "scanner": VulnScan(self.config, self.logger),
                "exploit": ExploitLab(self.config, self.logger, self.auth_manager),
                "cracker": HashCrack(self.config, self.logger),
                "forensics": ForensicKit(self.config, self.logger)
            }
            self.logger.info(f"Registered modules: {list(self.modules.keys())}")
        except Exception as e:
            self.logger.error(f"Failed to register modules: {e}")
            # Continue with partial modules if some fail to load
    
    async def run_recon(self, target: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """Run reconnaissance module"""
        if not self.auth_manager.check_authorization(target, "recon"):
            raise PermissionError(f"No authorization for target: {target}")
        
        self.logger.info(f"Starting reconnaissance on {target}")
        
        try:
            recon_module = self.modules.get("recon")
            if not recon_module:
                raise ValueError("Recon module not available")
            
            results = await recon_module.scan(target, options or {})
            
            self.results["recon"] = {
                "target": target,
                "timestamp": datetime.now().isoformat(),
                "data": results
            }
            
            self.auth_manager.log_action(target, "recon", "success")
            self.logger.info(f"Reconnaissance completed for {target}")
            return results
            
        except Exception as e:
            self.logger.error(f"Reconnaissance failed: {e}")
            self.auth_manager.log_action(target, "recon", f"failed: {e}")
            raise
    
    async def run_scan(self, target: str, scan_type: str = "full") -> Dict[str, Any]:
        """Run vulnerability scanner"""
        if not self.auth_manager.check_authorization(target, "scan"):
            raise PermissionError(f"No authorization for target: {target}")
        
        self.logger.info(f"Starting {scan_type} scan on {target}")
        
        try:
            scanner_module = self.modules.get("scanner")
            if not scanner_module:
                raise ValueError("Scanner module not available")
            
            results = await scanner_module.scan(target, scan_type)
            
            self.results["scan"] = {
                "target": target,
                "scan_type": scan_type,
                "timestamp": datetime.now().isoformat(),
                "data": results
            }
            
            self.auth_manager.log_action(target, f"scan:{scan_type}", "success")
            self.logger.info(f"Scan completed for {target}")
            return results
            
        except Exception as e:
            self.logger.error(f"Scan failed: {e}")
            self.auth_manager.log_action(target, f"scan:{scan_type}", f"failed: {e}")
            raise
    
    async def run_exploit(self, target: str, exploit_name: str, 
                         payload: Optional[str] = None) -> Dict[str, Any]:
        """Run exploit module (requires explicit authorization)"""
        if not self.auth_manager.check_authorization(target, "exploit"):
            raise PermissionError(f"No exploit authorization for target: {target}")
        
        if self.config.exploit.safe_mode and target not in self.config.exploit.allowed_targets:
            raise PermissionError(f"Target {target} not in allowed exploitation targets")
        
        self.logger.warning(f"Running exploit {exploit_name} on {target}")
        
        try:
            exploit_module = self.modules.get("exploit")
            if not exploit_module:
                raise ValueError("Exploit module not available")
            
            results = await exploit_module.run(target, exploit_name, payload)
            
            self.results["exploit"] = {
                "target": target,
                "exploit": exploit_name,
                "timestamp": datetime.now().isoformat(),
                "data": results
            }
            
            self.auth_manager.log_action(target, f"exploit:{exploit_name}", "success")
            return results
            
        except Exception as e:
            self.logger.error(f"Exploit failed: {e}")
            self.auth_manager.log_action(target, f"exploit:{exploit_name}", f"failed: {e}")
            raise
    
    async def run_cracker(self, hash_value: str, hash_type: str, 
                         wordlist: Optional[str] = None) -> Dict[str, Any]:
        """Run hash cracking module"""
        self.logger.info(f"Attempting to crack {hash_type} hash")
        
        try:
            cracker_module = self.modules.get("cracker")
            if not cracker_module:
                raise ValueError("Cracker module not available")
            
            results = await cracker_module.crack(hash_value, hash_type, wordlist)
            
            self.results["cracker"] = {
                "hash_type": hash_type,
                "timestamp": datetime.now().isoformat(),
                "success": results.get("success", False)
            }
            
            return results
            
        except Exception as e:
            self.logger.error(f"Hash cracking failed: {e}")
            raise
    
    async def run_forensics(self, file_path: str, analysis_type: str = "full") -> Dict[str, Any]:
        """Run forensic analysis module"""
        self.logger.info(f"Starting {analysis_type} forensic analysis on {file_path}")
        
        try:
            forensics_module = self.modules.get("forensics")
            if not forensics_module:
                raise ValueError("Forensics module not available")
            
            results = await forensics_module.analyze(file_path, analysis_type)
            
            self.results["forensics"] = {
                "file": file_path,
                "analysis_type": analysis_type,
                "timestamp": datetime.now().isoformat(),
                "data": results
            }
            
            return results
            
        except Exception as e:
            self.logger.error(f"Forensic analysis failed: {e}")
            raise
    
    def generate_report(self, report_type: str = "json") -> str:
        """Generate report from results"""
        report_data = {
            "generated_at": datetime.now().isoformat(),
            "results": self.results,
            "config": {
                "scanner": self.config.scanner.__dict__,
                "modules_available": list(self.modules.keys())
            }
        }
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if report_type == "json":
            report_path = self.config.reports_dir / f"report_{timestamp}.json"
            with open(report_path, 'w') as f:
                json.dump(report_data, f, indent=4)
            self.logger.info(f"Report generated: {report_path}")
            return str(report_path)
        
        elif report_type == "html":
            # Basic HTML report
            report_path = self.config.reports_dir / f"report_{timestamp}.html"
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>ByteBreaker Report</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    h1 {{ color: #333; }}
                    .section {{ margin-bottom: 20px; }}
                    pre {{ background-color: #f5f5f5; padding: 10px; }}
                </style>
            </head>
            <body>
                <h1>ByteBreaker Report</h1>
                <div class="section">
                    <h2>Generated: {report_data['generated_at']}</h2>
                    <pre>{json.dumps(report_data, indent=4)}</pre>
                </div>
            </body>
            </html>
            """
            with open(report_path, 'w') as f:
                f.write(html_content)
            self.logger.info(f"Report generated: {report_path}")
            return str(report_path)
        
        return ""
    
    def get_status(self) -> Dict[str, Any]:
        """Get framework status"""
        return {
            "modules_loaded": list(self.modules.keys()),
            "results_count": len(self.results),
            "authorizations": len(self.auth_manager.list_authorizations()),
            "config_valid": self.config.validate_config(),
            "thread_pool_active": True,
            "timestamp": datetime.now().isoformat()
        }
    
    def cleanup(self) -> None:
        """Cleanup resources"""
        try:
            self.executor.shutdown(wait=True)
            self.logger.info("Engine shutdown complete")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
