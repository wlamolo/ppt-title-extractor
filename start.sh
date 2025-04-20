#!/bin/bash

# Store the base directory
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Stopping all existing servers..."
pkill -f node
pkill -f python
pkill -f uvicorn

echo "Starting servers..."

# Start backend
echo "Starting backend server..."
cd "$BASE_DIR/backend"
source venv/bin/activate
uvicorn main:app --reload &
BACKEND_PID=$!

# Wait for backend to start
sleep 2
echo "Backend server running at http://localhost:8000"

# Start frontend
echo "Starting frontend server..."
cd "$BASE_DIR/frontend"
export PORT=5175  # Set specific port for frontend
npm run dev 