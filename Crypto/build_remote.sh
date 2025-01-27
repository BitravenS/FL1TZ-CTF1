#!/bin/bash

# Build Docker images
echo "Building DMZ..."
cd DMZ
./build_dmz.sh
cd ..

echo "Building Brainrot..."
cd brain_rot
sudo docker build -t brain-rot .
cd ..

echo "Building RS Ayyooo..."
cd rs_ayyooo
cd rsayo
sudo docker build -t rsayo .
cd ../rs_fast
sudo docker build -t rsayo-fast .
cd ../..

echo "Building Out of Sight..."
cd out_of_sight
sudo docker build -t out-of-sight .
cd ..

echo "Done!"
