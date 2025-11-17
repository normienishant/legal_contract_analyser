#!/bin/bash

# Run with Docker Compose
echo "Starting services with Docker Compose..."

if ! command -v docker-compose &> /dev/null; then
    echo "docker-compose not found. Please install Docker Compose."
    exit 1
fi

docker-compose up --build

