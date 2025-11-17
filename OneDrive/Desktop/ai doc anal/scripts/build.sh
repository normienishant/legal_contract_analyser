#!/bin/bash

# Build Docker images
echo "Building Docker images..."

echo "Building backend..."
cd backend
docker build -t contract-analyzer-backend:latest .

echo "Building frontend..."
cd ../frontend
docker build -t contract-analyzer-frontend:latest .

echo "Build complete!"

