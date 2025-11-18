#!/bin/bash
# Start script for Render deployment
cd /opt/render/project/src/backend
export PYTHONPATH=/opt/render/project/src/backend:$PYTHONPATH
python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT

