"""
ByteBreaker Web Dashboard Server
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
import os

app = FastAPI(title="ByteBreaker Dashboard", version="1.0.0")

# Setup templates - use absolute path
BASE_DIR = Path(__file__).parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Data storage
scan_history = []
vulnerability_history = []

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
            "total_scans": len(scan_history),
            "total_vulns": sum(v.get("total_found", 0) for v in vulnerability_history),
            "active_modules": 5
        }
    )

@app.get("/modules", response_class=HTMLResponse)
async def modules(request: Request):
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
async def reports(request: Request):
    """Reports page"""
    reports_list = []
    reports_dir = Path("data/reports")
    if reports_dir.exists():
        for report_file in reports_dir.glob("*"):
            reports_list.append({
                "name": report_file.name,
                "created": datetime.fromtimestamp(report_file.stat().st_mtime).isoformat(),
                "size": report_file.stat().st_size
            })
    
    return templates.TemplateResponse(
        "pages/reports.html",
        {
            "request": request,
            "active_page": "reports",
            "reports": reports_list
        }
    )

@app.get("/lab", response_class=HTMLResponse)
async def lab(request: Request):
    """Lab page"""
    return templates.TemplateResponse(
        "pages/lab.html",
        {"request": request, "active_page": "lab"}
    )

@app.get("/api/status")
async def api_status():
    """Get system status"""
    return {
        "status": "running",
        "modules": 5,
        "scans_completed": len(scan_history),
        "vulnerabilities_found": sum(v.get("total_found", 0) for v in vulnerability_history),
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)
