"""
Web Dashboard for ByteBreaker
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json
from datetime import datetime
from pathlib import Path

app = FastAPI(title="ByteBreaker Dashboard")
templates = Jinja2Templates(directory="templates")

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Render dashboard"""
    # Load results
    results = []
    reports_dir = Path("data/reports")
    if reports_dir.exists():
        for report_file in reports_dir.glob("*.json"):
            try:
                with open(report_file) as f:
                    report = json.load(f)
                    results.append(report)
            except:
                continue
    
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
    )
