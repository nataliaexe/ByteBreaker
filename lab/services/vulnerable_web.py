"""
Servidor web vulnerável para testes controlados
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime
import urllib.parse
import sqlite3
import os

class VulnerableWebHandler(BaseHTTPRequestHandler):
    """Handler para servidor web com vulnerabilidades intencionais"""
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        query = urllib.parse.parse_qs(parsed_path.query)
        
        # Vulnerável a XSS
        if path == '/search':
            search_term = query.get('q', [''])[0]
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(f"""
            <html>
            <body>
                <h1>Search Results</h1>
                <p>Results for: {search_term}</p>
                <form action="/search" method="GET">
                    <input type="text" name="q" placeholder="Search...">
                    <input type="submit" value="Search">
                </form>
            </body>
            </html>
            """.encode())
        
        # Vulnerável a SQL Injection
        elif path == '/user':
            user_id = query.get('id', ['1'])[0]
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            # Simulando SQL injection
            if "'" in user_id or "OR" in user_id.upper() or "1=1" in user_id:
                response = {
                    "error": "SQL injection detected",
                    "user": "admin",
                    "role": "administrator",
                    "password_hash": "0192023a7bbd73250516f069df18b500",
                    "sql_query": f"SELECT * FROM users WHERE id = '{user_id}'"
                }
            else:
                response = {
                    "user_id": user_id,
                    "username": f"user_{user_id}",
                    "role": "user"
                }
            
            self.wfile.write(json.dumps(response).encode())
        
        # Vulnerável a Path Traversal (corrigido)
        elif path == '/file':
            filename = query.get('name', ['test.txt'])[0]
            
            # Intencionalmente vulnerável - permite path traversal
            # Procura primeiro no diretório atual, depois em lab/data
            possible_paths = [
                filename,
                f"lab/data/{filename}",
                f"data/{filename}",
                filename.lstrip('../')
            ]
            
            file_found = False
            for file_path in possible_paths:
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                        self.send_response(200)
                        self.send_header('Content-Type', 'text/plain')
                        self.end_headers()
                        self.wfile.write(content.encode())
                        file_found = True
                        break
                except FileNotFoundError:
                    continue
                except Exception as e:
                    # Vulnerável a exposição de erros
                    self.send_response(500)
                    self.send_header('Content-Type', 'text/plain')
                    self.end_headers()
                    self.wfile.write(f"Error: {str(e)}".encode())
                    file_found = True
                    break
            
            if not file_found:
                self.send_response(404)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(b"File not found")
        
        # Página principal
        elif path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write("""
            <html>
            <body>
                <h1>Vulnerable Web Server</h1>
                <ul>
                    <li><a href="/search?q=test">XSS Test</a></li>
                    <li><a href="/user?id=1">SQL Injection Test</a></li>
                    <li><a href="/file?name=test.txt">Path Traversal Test</a></li>
                </ul>
                <p>Try these attacks:</p>
                <ul>
                    <li>XSS: /search?q=&lt;script&gt;alert(1)&lt;/script&gt;</li>
                    <li>SQLi: /user?id=1' OR '1'='1</li>
                    <li>Path Traversal: /file?name=../../etc/passwd</li>
                </ul>
            </body>
            </html>
            """.encode())
        
        # Diretório com listagem
        elif path == '/admin':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write("""
            <html>
            <body>
                <h1>Admin Directory</h1>
                <p>This directory has listing enabled</p>
                <p>Sensitive files:</p>
                <ul>
                    <li>users.txt - User credentials</li>
                    <li>config.ini - Configuration</li>
                </ul>
            </body>
            </html>
            """.encode())
        
        # Arquivo sensível exposto
        elif path == '/config':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"""
Database Configuration:
  host: localhost
  port: 5432
  username: admin
  password: admin123
  database: users_db

API Configuration:
  key: sk_test_123456789
  endpoint: /api/v1
  secret: super_secret_key_2024
""")
        
        # Simular arquivo de usuários
        elif path == '/users.txt':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"""
User Database (simulated):
  admin:admin123:administrator
  user1:password1:user
  user2:qwerty:user
  guest:guest123:guest
""")
        
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Not Found")
    
    def log_message(self, format, *args):
        """Log requests to file"""
        os.makedirs('lab/results', exist_ok=True)
        with open('lab/results/web_access.log', 'a') as f:
            f.write(f"{datetime.now().isoformat()} - {format % args}\n")

def start_vulnerable_server(port=8080):
    """Start vulnerable web server"""
    # Criar diretório de dados
    os.makedirs('lab/data', exist_ok=True)
    
    # Criar arquivos de teste
    if not os.path.exists('lab/data/test.txt'):
        with open('lab/data/test.txt', 'w') as f:
            f.write("This is a test file")
    
    if not os.path.exists('lab/data/secret.txt'):
        with open('lab/data/secret.txt', 'w') as f:
            f.write("Secret data: password=admin123")
    
    server = HTTPServer(('127.0.0.1', port), VulnerableWebHandler)
    print(f"Vulnerable web server running on http://127.0.0.1:{port}")
    print("Endpoints:")
    print("  /search?q=<script> - XSS")
    print("  /user?id=1' OR '1'='1 - SQL Injection")
    print("  /file?name=../../etc/passwd - Path Traversal")
    print("  /admin - Directory listing")
    print("  /config - Sensitive file")
    print("  /users.txt - User credentials")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")

if __name__ == "__main__":
    start_vulnerable_server()
