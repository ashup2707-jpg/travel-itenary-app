#!/bin/bash
# Start the backend server on http://localhost:8000
# Run this in a terminal and keep it open. In another terminal, run the frontend.

cd "$(dirname "$0")/backend"
echo "Starting backend at http://localhost:8000 ..."
echo "Press Ctrl+C to stop."
python3 main.py
