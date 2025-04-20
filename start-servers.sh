#!/bin/bash

# Define the project root directory
PROJECT_DIR="/Users/wlamolo/Projects/PPT Headlines"

# Start backend
cd "$PROJECT_DIR/backend"
source venv/bin/activate
uvicorn main:app --reload &

# Wait a moment for backend to start
sleep 2

# Start frontend
cd "$PROJECT_DIR/frontend"
npm run dev 