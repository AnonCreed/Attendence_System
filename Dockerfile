# Use Python 3.11 slim image (compatible with face_recognition)
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy your entire project into the container
COPY . /app

# Install system dependencies for dlib + opencv
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libboost-all-dev \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python packages
RUN pip install --upgrade pip wheel setuptools
RUN pip install numpy opencv-python dlib face-recognition
RUN pip install git+https://github.com/ageitgey/face_recognition_models

# Default command (runs enrollment first)
CMD ["python", "attendence/enrollment/enroll.py"]
