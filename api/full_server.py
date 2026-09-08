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

from core.engine import Engine
from core.config import Config
from core.logger import ByteBreakerLogger
from core.authorization import AuthorizationManager

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

# Templates
BASE_DIR = Path(__file__).parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Initialize
config = Config()
logger = ByteBreakerLogger()
engine = Engine(config)
auth_manager = AuthorizationManager()

# ============ FRONTEND PAGES ============

@app.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    """Landing page"""
    return templates.TemplateResponse(
        "pages/landing.html",
        {"request": request, "active_page": "home"}
    )

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Dashboard page"""
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

@app.get("/modules", response_class=HTMLResponse)
async def modules_page(request: Request):
    """Modules page"""
    return templates.TemplateResponse(
        "pages/modules.html",
        {"request": request, "active_page": "modules"}
    )

@app.get("/scan", response_class=HTMLResponse)
async def scan_page(request: Request):
    """Scan page"""
    return templates.TemplateResponse(
        "pages/scan.html",
        {"request": request, "active_page": "scan"}
    )

@app.get("/reports", response_class=HTMLResponse)
async def reports_page(request: Request):
    """Reports page"""
    return templates.TemplateResponse(
        "pages/reports.html",
        {"request": request, "active_page": "reports"}
    )

@app.get("/lab", response_class=HTMLResponse)
async def lab_page(request: Request):
    """Lab page"""
    return templates.TemplateResponse(
        "pages/lab.html",
        {"request": request, "active_page": "lab"}
    )

# ============ API ENDPOINTS ============

class CrackRequest(BaseModel):
    hash: str
    hash_type: str
    wordlist: Optional[str] = None

@app.get("/api/status")
async def get_status():
    """Get framework status"""
    status = engine.get_status()
    status["api_version"] = "3.0.0"
    status["dashboard"] = "active"
    return status

@app.get("/health")
async def health():
    """Health check"""
    return {"status": "healthy", "dashboard": True}

@app.post("/api/crack")
async def crack_hash(request: CrackRequest):
    """Crack hash"""
    try:
        results = await engine.run_cracker(
            request.hash,
            request.hash_type,
            request.wordlist
        )
        return results
    except Exception as e:
        return {"error": str(e)}

# ============ ENTRY POINT ============

if __name__ == "__main__":
    import re
    port_str = os.environ.get("PORT", "10000")
    match = re.search(r'\d+', port_str)
    port = int(match.group()) if match else 10000
    
    print(f"ByteBreaker rodando na porta {port}")
    print(f"Dashboard: http://localhost:{port}/")
    print(f"API Docs: http://localhost:{port}/api/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=port)
