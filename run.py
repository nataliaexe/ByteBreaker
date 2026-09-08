"""
Entry point for Render
"""
import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    print(f"Starting server on port {port}")
    uvicorn.run(
        "api.server:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info"
    )
