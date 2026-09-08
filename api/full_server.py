"""
ByteBreaker Full Server - API + Dashboard
"""
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

# Create FastAPI app
app = FastAPI(
    title="ByteBreaker Framework",
    description="Advanced Pentest Framework - API + Dashboard",
    version="3.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Templates - usar caminho absoluto
TEMPLATES_DIR = Path("/opt/render/project/src/templates")
if not TEMPLATES_DIR.exists():
    TEMPLATES_DIR = Path(__file__).parent.parent / "templates"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# ============ FRONTEND PAGES ============

@app.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    """Landing page"""
    try:
        return templates.TemplateResponse(
            "pages/landing.html",
            {"request": request, "active_page": "home"}
        )
    except Exception as e:
        return HTMLResponse(content=f"""
        <!DOCTYPE html>
        <html>
        <head><title>ByteBreaker</title></head>
        <body style="font-family: monospace; background: #0a0a1a; color: #00ff88; display: flex; justify-content: center; align-items: center; height: 100vh;">
            <div style="text-align: center;">
                <h1>BYTEBREAKER</h1>
                <p>Advanced Pentest Framework</p>
                <p>Status: <span style="color: #00ff88;">Online</span></p>
                <p><a href="/api/docs" style="color: #00ff88;">API Docs</a></p>
            </div>
        </body>
        </html>
        """)

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Dashboard page"""
    try:
        return templates.TemplateResponse(
            "pages/dashboard.html",
            {
                "request": request,
                "active_page": "dashboard",
                "total_scans": 12,
                "total_vulns": 10,
                "active_modules": 8
            }
        )
    except Exception as e:
        return HTMLResponse(content=f"<h1>Dashboard</h1><p>Error: {e}</p>")

@app.get("/modules", response_class=HTMLResponse)
async def modules_page(request: Request):
    """Modules page"""
    try:
        return templates.TemplateResponse(
            "pages/modules.html",
            {"request": request, "active_page": "modules"}
        )
    except Exception as e:
        return HTMLResponse(content=f"<h1>Modules</h1><p>Error: {e}</p>")

@app.get("/scan", response_class=HTMLResponse)
async def scan_page(request: Request):
    """Scan page"""
    try:
        return templates.TemplateResponse(
            "pages/scan.html",
            {"request": request, "active_page": "scan"}
        )
    except Exception as e:
        return HTMLResponse(content=f"<h1>Scan</h1><p>Error: {e}</p>")

@app.get("/reports", response_class=HTMLResponse)
async def reports_page(request: Request):
    """Reports page"""
    try:
        return templates.TemplateResponse(
            "pages/reports.html",
            {"request": request, "active_page": "reports"}
        )
    except Exception as e:
        return HTMLResponse(content=f"<h1>Reports</h1><p>Error: {e}</p>")

@app.get("/lab", response_class=HTMLResponse)
async def lab_page(request: Request):
    """Lab page"""
    try:
        return templates.TemplateResponse(
            "pages/lab.html",
            {"request": request, "active_page": "lab"}
        )
    except Exception as e:
        return HTMLResponse(content=f"<h1>Lab</h1><p>Error: {e}</p>")

# ============ API ENDPOINTS ============

class CrackRequest(BaseModel):
    hash: str
    hash_type: str
    wordlist: Optional[str] = None

@app.get("/api/status")
async def get_status():
    """Get framework status"""
    return {
        "status": "running",
        "api_version": "3.0.0",
        "modules": 8,
        "agents": 3,
        "dashboard": "active",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health():
    """Health check"""
    return {"status": "healthy", "dashboard": True}

@app.post("/api/crack")
async def crack_hash(request: CrackRequest):
    """Crack hash"""
    try:
        import hashlib
        # Simple hash cracking
        common = ["password", "123456", "admin123", "qwerty", "letmein"]
        hash_funcs = {
            "md5": hashlib.md5,
            "sha1": hashlib.sha1,
            "sha256": hashlib.sha256
        }
        
        hash_func = hash_funcs.get(request.hash_type)
        if not hash_func:
            return {"error": f"Unsupported hash type: {request.hash_type}"}
        
        for pwd in common:
            if hash_func(pwd.encode()).hexdigest() == request.hash.lower():
                return {
                    "success": True,
                    "password": pwd,
                    "hash_type": request.hash_type,
                    "attempts": common.index(pwd) + 1
                }
        
        return {"success": False, "message": "Hash not cracked with common passwords"}
    except Exception as e:
        return {"error": str(e)}

# ============ ENTRY POINT ============

if __name__ == "__main__":
    import re
    port_str = os.environ.get("PORT", "10000")
    match = re.search(r'\d+', port_str)
    port = int(match.group()) if match else 10000
    
    print(f"ByteBreaker rodando na porta {port}")
    print(f"Dashboard: /")
    print(f"API Docs: /api/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=port)
