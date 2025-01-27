#!/bin/bash

# Build Docker images
echo "Building Docker images..."
sudo docker build -f Dockerfile.lv1 -t lvl1 .
sudo docker build -f Dockerfile.lv2 -t lvl2 .
sudo docker build -f Dockerfile.lv3 -t lvl3 .
sudo docker build -f Dockerfile.lv4 -t lvl4 .

echo "Script completed."
