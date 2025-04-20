#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Build frontend
npm run build

# Move frontend build to backend/static
cd ..
mkdir -p backend/static
cp -r frontend/dist/* backend/static/

echo "Build completed successfully!" 