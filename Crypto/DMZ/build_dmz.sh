#!/bin/bash

# Build Docker images
echo "Building normal DMZ"
cd DMZ
./build.sh

echo "Building fast DMZ"

cd ../dmz_fast
./build.sh
echo "Script completed."
