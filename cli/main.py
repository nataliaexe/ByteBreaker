"""
ByteBreaker CLI - Main Entry Point
"""
import asyncio
import sys
import argparse
from typing import Optional, List
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.engine import Engine
from core.config import Config
from core.logger import ByteBreakerLogger
from core.authorization import AuthorizationManager


class ByteBreakerCLI:
    """Command-line interface for ByteBreaker"""
    
    def __init__(self):
        self.config = Config()
        self.logger = ByteBreakerLogger()
        self.engine = Engine(self.config)
        self.auth_manager = AuthorizationManager()
    
    def create_parser(self) -> argparse.ArgumentParser:
        """Create argument parser"""
        parser = argparse.ArgumentParser(
            description="ByteBreaker - Advanced Pentest Framework",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  bytebreaker authorize --target example.com --scope recon,scan --by "John Doe"
  bytebreaker recon --target example.com --options '{"port_scan": true}'
  bytebreaker scan --target example.com --type full
  bytebreaker crack --hash 5f4dcc3b5aa765d61d8327deb882cf99 --type md5
  bytebreaker forensics --file suspicious.exe --type full
  bytebreaker report --format json
  bytebreaker status
  bytebreaker authorizations
            """
        )
        
        # Subcommands
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Authorize command
        auth_parser = subparsers.add_parser('authorize', help='Authorize target for testing')
        auth_parser.add_argument('--target', required=True, help='Target IP or domain')
        auth_parser.add_argument('--scope', required=True, help='Comma-separated scope (recon,scan,exploit)')
        auth_parser.add_argument('--by', required=True, help='Authorizing person')
        auth_parser.add_argument('--days', type=int, default=30, help='Authorization validity in days')
        
        # Revoke authorization
        revoke_parser = subparsers.add_parser('revoke', help='Revoke authorization')
        revoke_parser.add_argument('--target', required=True, help='Target IP or domain')
        
        # Recon command
        recon_parser = subparsers.add_parser('recon', help='Run reconnaissance')
        recon_parser.add_argument('--target', required=True, help='Target IP or domain')
        recon_parser.add_argument('--options', help='JSON options for recon')
        
        # Scan command
        scan_parser = subparsers.add_parser('scan', help='Run vulnerability scan')
        scan_parser.add_argument('--target', required=True, help='Target IP or domain')
        scan_parser.add_argument('--type', default='full', 
                               choices=['full', 'quick', 'web', 'network'],
                               help='Scan type')
        
        # Exploit command
        exploit_parser = subparsers.add_parser('exploit', help='Run exploit (requires authorization)')
        exploit_parser.add_argument('--target', required=True, help='Target IP or domain')
        exploit_parser.add_argument('--name', required=True, help='Exploit name')
        exploit_parser.add_argument('--payload', help='Custom payload')
        
        # Crack command
        crack_parser = subparsers.add_parser('crack', help='Crack hash')
        crack_parser.add_argument('--hash', required=True, help='Hash to crack')
        crack_parser.add_argument('--type', required=True, choices=['md5', 'sha1', 'sha256'])
        crack_parser.add_argument('--wordlist', help='Custom wordlist path')
        
        # Forensics command
        forensics_parser = subparsers.add_parser('forensics', help='Run forensic analysis')
        forensics_parser.add_argument('--file', required=True, help='File to analyze')
        forensics_parser.add_argument('--type', default='full', 
                                    choices=['full', 'metadata', 'strings', 'hash'])
        
        # Report command
        report_parser = subparsers.add_parser('report', help='Generate report')
        report_parser.add_argument('--format', default='json', choices=['json', 'html', 'pdf'])
        
        # Status command
        status_parser = subparsers.add_parser('status', help='Show framework status')
        
        # Authorizations command
        list_auth_parser = subparsers.add_parser('authorizations', help='List authorizations')
        
        return parser
    
    async def execute_command(self, args: argparse.Namespace) -> None:
        """Execute CLI command"""
        try:
            if args.command == 'authorize':
                scope_list = args.scope.split(',')
                success = self.auth_manager.add_authorization(
                    args.target, scope_list, args.by, args.days
                )
                if success:
                    print(f"[+] Authorization added for {args.target}")
                else:
                    print("[-] Failed to add authorization")
            
            elif args.command == 'revoke':
                success = self.auth_manager.revoke_authorization(args.target)
                if success:
                    print(f"[+] Authorization revoked for {args.target}")
                else:
                    print(f"[-] No active authorization found for {args.target}")
            
            elif args.command == 'recon':
                options = json.loads(args.options) if args.options else {}
                results = await self.engine.run_recon(args.target, options)
                print(json.dumps(results, indent=4))
            
            elif args.command == 'scan':
                results = await self.engine.run_scan(args.target, args.type)
                print(json.dumps(results, indent=4))
            
            elif args.command == 'exploit':
                results = await self.engine.run_exploit(args.target, args.name, args.payload)
                print(json.dumps(results, indent=4))
            
            elif args.command == 'crack':
                results = await self.engine.run_cracker(args.hash, args.type, args.wordlist)
                print(json.dumps(results, indent=4))
            
            elif args.command == 'forensics':
                results = await self.engine.run_forensics(args.file, args.type)
                print(json.dumps(results, indent=4))
            
            elif args.command == 'report':
                report_path = self.engine.generate_report(args.format)
                print(f"[+] Report generated: {report_path}")
            
            elif args.command == 'status':
                status = self.engine.get_status()
                print(json.dumps(status, indent=4))
            
            elif args.command == 'authorizations':
                auths = self.auth_manager.list_authorizations()
                if auths:
                    print(json.dumps(auths, indent=4))
                else:
                    print("[!] No active authorizations")
            
            else:
                print("[!] No command specified. Use --help for usage.")
        
        except PermissionError as e:
            print(f"[-] Permission denied: {e}")
        except Exception as e:
            print(f"[-] Error: {e}")
            self.logger.error(f"Command execution failed: {e}")
    
    def run(self) -> None:
        """Run CLI"""
        parser = self.create_parser()
        args = parser.parse_args()
        
        if not args.command:
            parser.print_help()
            return
        
        try:
            asyncio.run(self.execute_command(args))
        except KeyboardInterrupt:
            print("\n[!] Operation cancelled by user")
        except Exception as e:
            print(f"[-] Unexpected error: {e}")
        finally:
            self.engine.cleanup()


def main():
    """Main entry point"""
    cli = ByteBreakerCLI()
    cli.run()


if __name__ == "__main__":
    main()
