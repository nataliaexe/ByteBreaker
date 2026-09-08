#!/bin/bash
# Start script for Render
cd /opt/render/project/src 2>/dev/null || cd "$(dirname "$0")"
exec uvicorn api.server:app --host 0.0.0.0 --port "${PORT:-10000}"
