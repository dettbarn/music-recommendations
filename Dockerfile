# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Install required Python packages
# Only requests is needed as external dependency
RUN pip install --no-cache-dir requests

# Create necessary directories
RUN mkdir -p /app/lastfm

# Copy Python scripts to container
COPY musicrecs.py .
COPY gui.py .
COPY docker-entrypoint.py .

# Make entrypoint script executable
RUN chmod +x docker-entrypoint.py

# Create volume mount points for data exchange with host
VOLUME ["/app/data", "/app/lastfm"]

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Use the entrypoint script to handle file management
ENTRYPOINT ["python", "docker-entrypoint.py"]

# Default arguments (can be overridden)
CMD []
