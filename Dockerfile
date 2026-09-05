FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for TTS and audio processing
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy application files
COPY backend ./backend/
COPY frontend ./frontend/
COPY models ./models/

# Install Python dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

# Create runtime directories
RUN mkdir -p /app/backend/uploads /app/backend/references

# Expose ports
EXPOSE 5001

# Start the Looking Glass Web Alternative server
CMD ["python", "-m", "backend.app"]
