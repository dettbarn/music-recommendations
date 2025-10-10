#!/bin/bash

# Docker Example Script for Music Recommendations
# This script demonstrates how to set up and run the music recommendations in Docker

set -e  # Exit on any error

echo "=== Music Recommendations Docker Setup ==="
echo

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed or not in PATH"
    echo "Please install Docker first: https://docs.docker.com/get-docker/"
    exit 1
fi

# Create directory structure
echo "1. Creating directory structure..."
mkdir -p ./host-data/lastfm

# Check if API key exists
if [ ! -f "./host-data/lastfm/.api_key" ]; then
    echo
    echo "2. Setting up Last.fm API key..."
    echo "Please enter your Last.fm API key:"
    read -r api_key
    echo "$api_key" > ./host-data/lastfm/.api_key
    echo "API key saved to ./host-data/lastfm/.api_key"
else
    echo "2. API key already exists at ./host-data/lastfm/.api_key"
fi

# Create example input file if it doesn't exist
if [ ! -f "./host-data/input.txt" ]; then
    echo
    echo "3. Creating example input file..."
    cat > ./host-data/input.txt << 'EOF'
The Beatles%3
Radiohead%2
Pink Floyd%2.5
Led Zeppelin%2.8
Queen%2.2
The Rolling Stones%2.1
EOF
    echo "Example input file created at ./host-data/input.txt"
    echo "You can edit this file to add your favorite artists."
else
    echo "3. Input file already exists at ./host-data/input.txt"
fi

echo
echo "4. Building Docker image..."
docker build -t music-recommendations .

echo
echo "5. Running music recommendations..."
docker run --rm \
  -v "$(pwd)/host-data:/app/data" \
  -v "$(pwd)/host-data/lastfm:/app/lastfm" \
  music-recommendations

echo
echo "=== Results ==="
if [ -f "./host-data/output.txt" ]; then
    echo "Recommendations saved to ./host-data/output.txt"
    echo "First 10 recommendations:"
    head -10 ./host-data/output.txt
else
    echo "No output file generated. Check for errors above."
fi

if [ -f "./host-data/outroot.txt" ]; then
    echo
    echo "Detailed analysis saved to ./host-data/outroot.txt"
fi

echo
echo "=== Setup Complete ==="
echo "You can now:"
echo "- Edit ./host-data/input.txt to change your favorite artists"
echo "- Run: docker run --rm -v \"\$(pwd)/host-data:/app/data\" -v \"\$(pwd)/host-data/lastfm:/app/lastfm\" music-recommendations"
echo "- For interactive mode: docker run --rm -it -v \"\$(pwd)/host-data:/app/data\" -v \"\$(pwd)/host-data/lastfm:/app/lastfm\" music-recommendations -i"
