"""
ByteBreaker API Routes
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Optional
from pydantic import BaseModel

router = APIRouter()


class ExploitRequest(BaseModel):
    target: str
    exploit_name: str
    payload: Optional[str] = None


@router.post("/exploit")
async def run_exploit(request: ExploitRequest):
    """Run exploit (requires authorization)"""
    try:
        # Import here to avoid circular imports
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent.parent))
        
        from core.engine import Engine
        engine = Engine()
        
        results = await engine.run_exploit(
            request.target,
            request.exploit_name,
            request.payload
        )
        return results
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/exploits")
async def list_exploits():
    """List available exploits"""
    try:
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent.parent))
        
        from modules.exploit import ExploitLab
        exploit_module = ExploitLab(None, None)
        
        return {"exploits": exploit_module.list_exploits()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
