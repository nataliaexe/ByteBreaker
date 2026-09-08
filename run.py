"""
Entry point for Render - Full Server with Dashboard
"""
import os
import re
import uvicorn

if __name__ == "__main__":
    port_str = os.environ.get("PORT", "10000")
    match = re.search(r'\d+', port_str)
    port = int(match.group()) if match else 10000
    
    print(f"Starting ByteBreaker on port {port}")
    print(f"Dashboard: /")
    print(f"API Docs: /api/docs")
    
    uvicorn.run(
        "api.full_server:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info"
    )
