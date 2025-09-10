#!/bin/bash
# start.sh

# Ensure repo root is in Python path
export PYTHONPATH="$(pwd)"

# Optional: debug path (can remove later)
echo "PYTHONPATH=$PYTHONPATH"
ls -la
python -c "import sys; print(sys.path)"

# Start Uvicorn
uvicorn app.main:app --host 0.0.0.0 --port $PORT
