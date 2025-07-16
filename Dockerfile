FROM python:3.11-slim

WORKDIR /app

# Required for OpenCV and ONNX
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    gunicorn

COPY . .

# Ensure folders
RUN mkdir -p inputs output

# Expose API port
EXPOSE 8000

# Run with 4 parallel worker processes
CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000"]
