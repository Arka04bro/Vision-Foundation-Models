FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /main

# Update and install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg libsm6 libxext6 git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies from requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files into the working directory
COPY src/ ./src/
COPY model/ ./model/ # Copy the entire model directory
COPY .env .

# Set environment variable
ENV PYTHONUNBUFFERED=1

# Default command to run when the container starts
# Choose the script you want to run:

# To run the ESP32-CAM script:
# CMD ["python", "src/ESP32-CAM.py"]

# To run the WEBCAM script (uncomment the line below and comment the one above):
CMD ["python", "src/WEBCAM.py"]
