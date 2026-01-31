#!/bin/bash
# Start the frontend on http://localhost:3000
# Run the backend first (./start_backend.sh) in another terminal.

cd "$(dirname "$0")/frontend"
echo "Starting frontend at http://localhost:3000 ..."
echo "Press Ctrl+C to stop."
npm run dev
