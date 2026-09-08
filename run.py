"""
Entry point for Render
"""
import os
import uvicorn

if __name__ == "__main__":
    # Try to get port, fallback to 10000
    port_str = os.environ.get("PORT", "10000")
    
    # Clean port string - extract only digits
    import re
    match = re.search(r'\d+', port_str)
    port = int(match.group()) if match else 10000
    
    print(f"Starting ByteBreaker on port {port}")
    
    uvicorn.run(
        "api.server:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info"
    )
