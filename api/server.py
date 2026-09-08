"""
ByteBreaker API Server - Render Compatible
"""
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
import uvicorn
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

from core.engine import Engine
from core.config import Config
from core.logger import ByteBreakerLogger
from core.authorization import AuthorizationManager


# Request/Response models
class AuthorizeRequest(BaseModel):
    target: str = Field(..., description="Target IP or domain")
    scope: List[str] = Field(..., description="Testing scope")
    authorized_by: str = Field(..., description="Authorizing person")
    days: int = Field(30, description="Authorization validity in days")

class ReconRequest(BaseModel):
    target: str = Field(..., description="Target IP or domain")
    options: Optional[Dict[str, Any]] = Field(None, description="Recon options")

class ScanRequest(BaseModel):
    target: str = Field(..., description="Target IP or domain")
    scan_type: str = Field("full", description="Scan type")

class CrackRequest(BaseModel):
    hash: str = Field(..., description="Hash to crack")
    hash_type: str = Field(..., description="Hash type (md5, sha1, sha256)")
    wordlist: Optional[str] = Field(None, description="Custom wordlist path")

class ForensicsRequest(BaseModel):
    file_path: str = Field(..., description="File to analyze")
    analysis_type: str = Field("full", description="Analysis type")


# Create FastAPI app
app = FastAPI(
    title="ByteBreaker API",
    description="Advanced Pentest Framework API",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
config = Config()
logger = ByteBreakerLogger()
engine = Engine(config)
auth_manager = AuthorizationManager()


@app.get("/", response_class=HTMLResponse)
async def root():
    """API root endpoint with HTML"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ByteBreaker API</title>
        <style>
            body { font-family: 'Courier New', monospace; background: #0a0a1a; color: #00ff88; 
                   display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .container { text-align: center; }
            h1 { font-size: 3em; margin-bottom: 10px; }
            p { color: #a0a0a0; }
            a { color: #00ff88; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>BYTEBREAKER</h1>
            <p>Advanced Pentest Framework API</p>
            <p>Status: <span style="color: #00ff88;">Online</span></p>
            <p><a href="/docs">API Documentation</a> | <a href="/status">Status</a></p>
        </div>
    </body>
    </html>
    """


@app.get("/status")
async def get_status():
    """Get framework status"""
    try:
        status = engine.get_status()
        status["api_version"] = "2.0.0"
        status["deployed_on"] = "Render"
        return JSONResponse(content=status)
    except Exception as e:
        logger.error(f"Status endpoint failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint for Render"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/authorize")
async def authorize(request: AuthorizeRequest):
    """Authorize target for testing"""
    try:
        success = auth_manager.add_authorization(
            request.target,
            request.scope,
            request.authorized_by,
            request.days
        )
        if success:
            return {"status": "success", "message": f"Authorized {request.target}"}
        else:
            raise HTTPException(status_code=400, detail="Failed to add authorization")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Authorization failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/authorizations")
async def list_authorizations():
    """List all active authorizations"""
    try:
        auths = auth_manager.list_authorizations()
        return {"authorizations": auths}
    except Exception as e:
        logger.error(f"List authorizations failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/recon")
async def run_recon(request: ReconRequest):
    """Run reconnaissance"""
    try:
        results = await engine.run_recon(request.target, request.options)
        return results
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.error(f"Recon failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/scan")
async def run_scan(request: ScanRequest):
    """Run vulnerability scan"""
    try:
        results = await engine.run_scan(request.target, request.scan_type)
        return results
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.error(f"Scan failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/crack")
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
        logger.error(f"Hash cracking failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/forensics")
async def run_forensics(request: ForensicsRequest):
    """Run forensic analysis"""
    try:
        results = await engine.run_forensics(
            request.file_path, 
            request.analysis_type
        )
        return results
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Forensics failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/report")
async def generate_report(format: str = "json"):
    """Generate report"""
    try:
        report_path = engine.generate_report(format)
        if report_path:
            return {"status": "success", "report_path": report_path}
        else:
            raise HTTPException(status_code=400, detail="Unsupported format")
    except Exception as e:
        logger.error(f"Report generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    engine.cleanup()


# For Render - get port from environment
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
