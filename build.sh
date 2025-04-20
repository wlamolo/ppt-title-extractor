#!/bin/bash

echo "Building frontend..."
cd frontend
npm install
npm run build
cd ..

echo "Setting up backend..."
cd backend
pip install -r requirements.txt

echo "Starting server..."
uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} 