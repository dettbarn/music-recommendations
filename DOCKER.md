# Docker Usage Guide

This guide explains how to run the music recommendations script using Docker, making it independent of your local machine setup.

## Prerequisites

- Docker installed on your system
- Last.fm API key

## Setup

### 1. Prepare the API Key

Create a directory structure on your host machine:

```bash
mkdir -p ./host-data/lastfm
```

Place your Last.fm API key in `./host-data/lastfm/.api_key`:

```bash
echo "your_lastfm_api_key_here" > ./host-data/lastfm/.api_key
```

### 2. Prepare Input File

Create your input file with artist names and weights:

```bash
cat > ./host-data/input.txt << EOF
The Beatles%3
Radiohead%2
Muse%1.5
Pink Floyd%2.5
EOF
```

## Building the Docker Image

Build the Docker image from the project directory:

```bash
docker build -t music-recommendations .
```

## Running the Container

### File Mode (Recommended)

Run the container with volume mounts to share files between host and container:

```bash
docker run --rm \
  -v "$(pwd)/host-data:/app/data" \
  -v "$(pwd)/host-data/lastfm:/app/lastfm" \
  music-recommendations
```

The container will automatically:

- Look for `input.txt` in the mounted data directory
- Copy output files (`output.txt` and `outroot.txt`) back to the data directory

### Interactive Mode

For interactive input mode:

```bash
docker run --rm -it \
  -v "$(pwd)/host-data:/app/data" \
  -v "$(pwd)/host-data/lastfm:/app/lastfm" \
  music-recommendations -i
```

## Output Files

After running, you'll find the output files in your `host-data` directory:

- `output.txt` - Artist recommendations with weights
- `outroot.txt` - Detailed information about recommendation sources

## Volume Mounts Explained

- `-v "$(pwd)/host-data:/app/data"` - Mounts host data directory for input/output files
- `-v "$(pwd)/host-data/lastfm:/app/lastfm"` - Mounts the lastfm directory containing the API key

## Troubleshooting

### Permission Issues

If you encounter permission issues, ensure the host directories are readable:

```bash
chmod -R 755 ./host-data
```

### API Key Issues

Verify your API key file:

```bash
cat ./host-data/lastfm/.api_key
```

### Input File Format

Ensure your input file follows the correct format:

```
Artist Name%Weight
Another Artist%Weight
```

## Example Complete Workflow

```bash
# 1. Create directory structure
mkdir -p ./host-data/lastfm

# 2. Add your API key
echo "your_actual_api_key_here" > ./host-data/lastfm/.api_key

# 3. Create input file
cat > ./host-data/input.txt << EOF
The Beatles%3
Radiohead%2
Muse%1.5
EOF

# 4. Build Docker image
docker build -t music-recommendations .

# 5. Run the container
docker run --rm \
  -v "$(pwd)/host-data:/app/data" \
  -v "$(pwd)/host-data/lastfm:/app/lastfm" \
  music-recommendations

# 6. Check results
cat ./host-data/output.txt
cat ./host-data/outroot.txt
```

## Windows Users

For Windows Command Prompt, replace `$(pwd)` with `%cd%`:

```cmd
docker run --rm -v "%cd%/host-data:/app/data" -v "%cd%/host-data/lastfm:/app/lastfm" music-recommendations
```

For Windows PowerShell, use `${PWD}`:

```powershell
docker run --rm -v "${PWD}/host-data:/app/data" -v "${PWD}/host-data/lastfm:/app/lastfm" music-recommendations
```
