FROM python:3.13.3-alpine

# Set working directory
WORKDIR /app

# Copy source code
COPY . .

# Install build tools and dependencies for common Python packages
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
    lapack-dev \
    && pip install --upgrade pip \
    && pip install nvidia-pyindex \
    && pip install nvidia-nccl-cu12 \
    && pip install --no-cache-dir -r requirements.txt
# Command to run the app
CMD ["python3", "app.py"]