@echo off
REM Docker Example Script for Music Recommendations (Windows)
REM This script demonstrates how to set up and run the music recommendations in Docker

echo === Music Recommendations Docker Setup ===
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo Error: Docker is not installed or not in PATH
    echo Please install Docker Desktop: https://docs.docker.com/desktop/windows/
    pause
    exit /b 1
)

REM Create directory structure
echo 1. Creating directory structure...
if not exist "host-data\lastfm" mkdir host-data\lastfm

REM Check if API key exists
if not exist "host-data\lastfm\.api_key" (
    echo.
    echo 2. Setting up Last.fm API key...
    set /p api_key="Please enter your Last.fm API key: "
    echo !api_key! > host-data\lastfm\.api_key
    echo API key saved to host-data\lastfm\.api_key
) else (
    echo 2. API key already exists at host-data\lastfm\.api_key
)

REM Create example input file if it doesn't exist
if not exist "host-data\input.txt" (
    echo.
    echo 3. Creating example input file...
    (
        echo The Beatles%%3
        echo Radiohead%%2
        echo Pink Floyd%%2.5
        echo Led Zeppelin%%2.8
        echo Queen%%2.2
        echo The Rolling Stones%%2.1
    ) > host-data\input.txt
    echo Example input file created at host-data\input.txt
    echo You can edit this file to add your favorite artists.
) else (
    echo 3. Input file already exists at host-data\input.txt
)

echo.
echo 4. Building Docker image...
docker build -t music-recommendations .

echo.
echo 5. Running music recommendations...
docker run --rm -v "%cd%\host-data:/app/data" -v "%cd%\host-data\lastfm:/app/lastfm" music-recommendations

echo.
echo === Results ===
if exist "host-data\output.txt" (
    echo Recommendations saved to host-data\output.txt
    echo First 10 recommendations:
    powershell "Get-Content host-data\output.txt | Select-Object -First 10"
) else (
    echo No output file generated. Check for errors above.
)

if exist "host-data\outroot.txt" (
    echo.
    echo Detailed analysis saved to host-data\outroot.txt
)

echo.
echo === Setup Complete ===
echo You can now:
echo - Edit host-data\input.txt to change your favorite artists
echo - Run: docker run --rm -v "%%cd%%\host-data:/app/data" -v "%%cd%%\host-data\lastfm:/app/lastfm" music-recommendations
echo - For interactive mode: docker run --rm -it -v "%%cd%%\host-data:/app/data" -v "%%cd%%\host-data\lastfm:/app/lastfm" music-recommendations -i

pause
