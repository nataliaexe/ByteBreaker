"""
ByteBreaker CLI v2 - Enhanced
"""
import asyncio
import sys
import argparse
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.engine_v2 import EnhancedEngine
from core.config import Config
from core.logger import ByteBreakerLogger
from core.authorization import AuthorizationManager


class ByteBreakerCLIv2:
    """Enhanced CLI"""
    
    def __init__(self):
        self.config = Config()
        self.logger = ByteBreakerLogger()
        self.engine = EnhancedEngine(self.config)
        self.auth_manager = AuthorizationManager()
    
    def create_parser(self) -> argparse.ArgumentParser:
        """Create parser with all commands"""
        parser = argparse.ArgumentParser(
            description="ByteBreaker - Advanced Pentest Framework v2",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  python cli/main_v2.py authorize --target example.com --scope recon,scan --by "Name"
  python cli/main_v2.py recon --target example.com
  python cli/main_v2.py scan --target example.com --type web
  python cli/main_v2.py dirb --target example.com
  python cli/main_v2.py osint --target example.com
  python cli/main_v2.py fingerprint --target example.com
  python cli/main_v2.py sniff --interface eth0 --count 100
  python cli/main_v2.py crack --hash <hash> --type md5
  python cli/main_v2.py forensics --file file.txt --type full
  python cli/main_v2.py exploit --target example.com --name command_injection
  python cli/main_v2.py report --format json
  python cli/main_v2.py pdf
  python cli/main_v2.py status
            """
        )
        
        subparsers = parser.add_subparsers(dest='command')
        
        # Authorize
        auth_parser = subparsers.add_parser('authorize')
        auth_parser.add_argument('--target', required=True)
        auth_parser.add_argument('--scope', required=True)
        auth_parser.add_argument('--by', required=True)
        auth_parser.add_argument('--days', type=int, default=30)
        
        # Revoke
        revoke_parser = subparsers.add_parser('revoke')
        revoke_parser.add_argument('--target', required=True)
        
        # Recon
        recon_parser = subparsers.add_parser('recon')
        recon_parser.add_argument('--target', required=True)
        recon_parser.add_argument('--options', help='JSON options')
        
        # Scan
        scan_parser = subparsers.add_parser('scan')
        scan_parser.add_argument('--target', required=True)
        scan_parser.add_argument('--type', default='full')
        
        # Exploit
        exploit_parser = subparsers.add_parser('exploit')
        exploit_parser.add_argument('--target', required=True)
        exploit_parser.add_argument('--name', required=True)
        exploit_parser.add_argument('--payload')
        
        # Crack
        crack_parser = subparsers.add_parser('crack')
        crack_parser.add_argument('--hash', required=True)
        crack_parser.add_argument('--type', required=True)
        crack_parser.add_argument('--wordlist')
        
        # Forensics
        forensics_parser = subparsers.add_parser('forensics')
        forensics_parser.add_argument('--file', required=True)
        forensics_parser.add_argument('--type', default='full')
        
        # Directory bruteforce
        dirb_parser = subparsers.add_parser('dirb')
        dirb_parser.add_argument('--target', required=True)
        
        # OSINT
        osint_parser = subparsers.add_parser('osint')
        osint_parser.add_argument('--target', required=True)
        
        # Network sniffing
        sniff_parser = subparsers.add_parser('sniff')
        sniff_parser.add_argument('--interface', default='eth0')
        sniff_parser.add_argument('--count', type=int, default=100)
        
        # OS fingerprinting
        fingerprint_parser = subparsers.add_parser('fingerprint')
        fingerprint_parser.add_argument('--target', required=True)
        
        # Report
        report_parser = subparsers.add_parser('report')
        report_parser.add_argument('--format', default='json', choices=['json', 'html'])
        
        # PDF report
        pdf_parser = subparsers.add_parser('pdf')
        
        # Status
        status_parser = subparsers.add_parser('status')
        
        # Authorizations
        auths_parser = subparsers.add_parser('authorizations')
        
        return parser
    
    async def execute(self, args):
        """Execute command"""
        try:
            if args.command == 'authorize':
                scope_list = args.scope.split(',')
                success = self.auth_manager.add_authorization(args.target, scope_list, args.by, args.days)
                print(f"[+] Authorized {args.target}" if success else "[-] Failed")
            
            elif args.command == 'revoke':
                success = self.auth_manager.revoke_authorization(args.target)
                print(f"[+] Revoked {args.target}" if success else "[-] Not found")
            
            elif args.command == 'recon':
                options = json.loads(args.options) if args.options else {}
                results = await self.engine.run_recon(args.target, options)
                print(json.dumps(results, indent=2))
            
            elif args.command == 'scan':
                results = await self.engine.run_scan(args.target, args.type)
                print(json.dumps(results, indent=2))
            
            elif args.command == 'exploit':
                results = await self.engine.run_exploit(args.target, args.name, args.payload)
                print(json.dumps(results, indent=2))
            
            elif args.command == 'crack':
                results = await self.engine.run_cracker(args.hash, args.type, args.wordlist)
                print(json.dumps(results, indent=2))
            
            elif args.command == 'forensics':
                results = await self.engine.run_forensics(args.file, args.type)
                print(json.dumps(results, indent=2))
            
            elif args.command == 'dirb':
                results = await self.engine.run_dir_bruteforce(args.target)
                print(json.dumps(results, indent=2))
            
            elif args.command == 'osint':
                if 'osint' in self.engine.agents:
                    agent = self.engine.agents['osint']
                    results = await agent.search_domain(args.target)
                    print(json.dumps(results, indent=2))
                else:
                    print("OSINT agent not available")
            
            elif args.command == 'sniff':
                results = await self.engine.run_network_sniff(args.interface, args.count)
                print(json.dumps(results, indent=2))
            
            elif args.command == 'fingerprint':
                results = await self.engine.run_os_fingerprint(args.target)
                print(json.dumps(results, indent=2))
            
            elif args.command == 'report':
                path = self.engine.generate_report(args.format)
                print(f"[+] Report: {path}")
            
            elif args.command == 'pdf':
                path = self.engine.generate_pdf_report()
                print(f"[+] PDF Report: {path}")
            
            elif args.command == 'status':
                status = self.engine.get_status()
                print(json.dumps(status, indent=2))
            
            elif args.command == 'authorizations':
                auths = self.auth_manager.list_authorizations()
                print(json.dumps(auths, indent=2))
            
        except PermissionError as e:
            print(f"[-] Permission denied: {e}")
        except Exception as e:
            print(f"[-] Error: {e}")
    
    def run(self):
        """Run CLI"""
        parser = self.create_parser()
        args = parser.parse_args()
        
        if not args.command:
            parser.print_help()
            return
        
        try:
            asyncio.run(self.execute(args))
        except KeyboardInterrupt:
            print("\n[!] Cancelled")
        finally:
            self.engine.cleanup()


if __name__ == "__main__":
    cli = ByteBreakerCLIv2()
    cli.run()
