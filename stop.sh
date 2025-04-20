#!/bin/bash

echo "Stopping all servers..."
pkill -f node
pkill -f python
pkill -f uvicorn

echo "All servers stopped." 