"""
ByteBreaker Interactive CLI
"""
import asyncio
import sys
import json
from pathlib import Path
from typing import Optional, Dict, Any

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.engine import Engine
from core.config import Config
from core.logger import ByteBreakerLogger
from core.authorization import AuthorizationManager


class InteractiveCLI:
    """Interactive command-line interface"""
    
    def __init__(self):
        self.config = Config()
        self.logger = ByteBreakerLogger()
        self.engine = Engine(self.config)
        self.auth_manager = AuthorizationManager()
        self.running = True
        self.commands = {
            "help": self.show_help,
            "authorize": self.authorize_target,
            "recon": self.run_recon,
            "scan": self.run_scan,
            "crack": self.crack_hash,
            "forensics": self.run_forensics,
            "status": self.show_status,
            "authorizations": self.list_authorizations,
            "report": self.generate_report,
            "exit": self.exit_cli,
            "quit": self.exit_cli
        }
    
    def show_help(self):
        """Show help message"""
        print("""
ByteBreaker Interactive Commands:
  help              - Show this help
  authorize         - Authorize target for testing
  recon             - Run reconnaissance
  scan              - Run vulnerability scan
  crack             - Crack hash
  forensics         - Run forensic analysis
  status            - Show framework status
  authorizations    - List authorizations
  report            - Generate report
  exit/quit         - Exit interactive mode

Usage examples:
  authorize example.com recon,scan "John Doe"
  recon example.com
  scan example.com full
  crack 5f4dcc3b5aa765d61d8327deb882cf99 md5
  forensics /path/to/file full
        """)
    
    def authorize_target(self, args: list):
        """Authorize target"""
        if len(args) < 3:
            print("Usage: authorize <target> <scope1,scope2> <authorized_by> [days]")
            return
        
        target = args[0]
        scope = args[1].split(',')
        authorized_by = args[2]
        days = int(args[3]) if len(args) > 3 else 30
        
        success = self.auth_manager.add_authorization(target, scope, authorized_by, days)
        if success:
            print(f"Authorized {target}")
        else:
            print(f"Failed to authorize {target}")
    
    def run_recon(self, args: list):
        """Run reconnaissance"""
        if len(args) < 1:
            print("Usage: recon <target> [options_json]")
            return
        
        target = args[0]
        options = json.loads(args[1]) if len(args) > 1 else {}
        
        try:
            results = asyncio.run(self.engine.run_recon(target, options))
            print(json.dumps(results, indent=2))
        except Exception as e:
            print(f"Recon failed: {e}")
    
    def run_scan(self, args: list):
        """Run vulnerability scan"""
        if len(args) < 1:
            print("Usage: scan <target> [scan_type]")
            return
        
        target = args[0]
        scan_type = args[1] if len(args) > 1 else "full"
        
        try:
            results = asyncio.run(self.engine.run_scan(target, scan_type))
            print(json.dumps(results, indent=2))
        except Exception as e:
            print(f"Scan failed: {e}")
    
    def crack_hash(self, args: list):
        """Crack hash"""
        if len(args) < 2:
            print("Usage: crack <hash> <hash_type> [wordlist]")
            return
        
        hash_value = args[0]
        hash_type = args[1]
        wordlist = args[2] if len(args) > 2 else None
        
        try:
            results = asyncio.run(self.engine.run_cracker(hash_value, hash_type, wordlist))
            print(json.dumps(results, indent=2))
        except Exception as e:
            print(f"Cracking failed: {e}")
    
    def run_forensics(self, args: list):
        """Run forensic analysis"""
        if len(args) < 1:
            print("Usage: forensics <file_path> [analysis_type]")
            return
        
        file_path = args[0]
        analysis_type = args[1] if len(args) > 1 else "full"
        
        try:
            results = asyncio.run(self.engine.run_forensics(file_path, analysis_type))
            print(json.dumps(results, indent=2))
        except Exception as e:
            print(f"Forensics failed: {e}")
    
    def show_status(self):
        """Show framework status"""
        status = self.engine.get_status()
        print(json.dumps(status, indent=2))
    
    def list_authorizations(self):
        """List authorizations"""
        auths = self.auth_manager.list_authorizations()
        if auths:
            print(json.dumps(auths, indent=2))
        else:
            print("No active authorizations")
    
    def generate_report(self):
        """Generate report"""
        report_path = self.engine.generate_report("json")
        if report_path:
            print(f"Report generated: {report_path}")
        else:
            print("Failed to generate report")
    
    def exit_cli(self):
        """Exit interactive mode"""
        print("Exiting ByteBreaker...")
        self.running = False
        self.engine.cleanup()
    
    def run(self):
        """Run interactive CLI"""
        print("""
========================================
    ByteBreaker Interactive Console
    Type 'help' for available commands
    Type 'exit' to quit
========================================
        """)
        
        while self.running:
            try:
                user_input = input("\nbytebreaker> ").strip()
                
                if not user_input:
                    continue
                
                parts = user_input.split()
                command = parts[0].lower()
                args = parts[1:] if len(parts) > 1 else []
                
                if command in self.commands:
                    if args:
                        self.commands[command](args)
                    else:
                        self.commands[command]()
                else:
                    print(f"Unknown command: {command}")
                    print("Type 'help' for available commands")
            
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit")
            except Exception as e:
                print(f"Error: {e}")


def main():
    """Main entry point for interactive CLI"""
    cli = InteractiveCLI()
    cli.run()


if __name__ == "__main__":
    main()
