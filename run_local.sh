#!/bin/bash
# Run the app locally: start backend and frontend in two terminals.
# Usage: ./run_local.sh   (prints commands) or run each block in a separate terminal.

set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
echo "Project root: $ROOT"
echo ""
echo "Run these in TWO separate terminals:"
echo ""
echo "--- Terminal 1 (Backend) ---"
echo "  cd \"$ROOT/backend\""
echo "  python3 main.py"
echo ""
echo "--- Terminal 2 (Frontend) ---"
echo "  cd \"$ROOT/frontend\""
echo "  npm install && npm run dev"
echo ""
echo "Then open: http://localhost:3000"
echo "Backend API: http://localhost:8000"
echo "Readiness:   http://localhost:8000/health/ready"
echo ""
