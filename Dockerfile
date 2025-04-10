# Use a stable base image
FROM python:3.10-alpine

# Set working directory
WORKDIR /app

# Copy local project files to the container
COPY . .

# Install system dependencies
RUN apk add --no-cache \
    build-base \
    cmake \
    libffi-dev \
    musl-dev \
    gcc \
    g++ \
    python3-dev \
    py3-pip \
    libxml2-dev \
    libxslt-dev \
    postgresql-dev \
    openblas-dev \
    freetype-dev \
    lapack-dev

# Upgrade pip and install requirements
RUN pip install --upgrade pip \
    && pip install --extra-index-url https://pypi.nvidia.com nvidia-nccl-cu12 \
    && pip install --no-cache-dir -r requirements.txt

# Set the command to run your app (replace this as needed)
CMD ["python", "app.py"]
