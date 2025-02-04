#!/bin/bash

# Stop and remove any existing containers
echo "Stopping and removing existing containers..."
docker-compose down

# Build and start the containers
echo "Building and starting the containers..."
docker-compose up --build -d

# Provide instructions to access the challenge
echo "CTF challenge is now running!"
echo "Access it at: http://localhost:8080"