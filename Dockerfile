FROM python:3.10-alpine

WORKDIR /app

COPY . .

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

# Upgrade pip, install NVIDIA index first, then install other dependencies
RUN pip install --upgrade pip \
    && pip install nvidia-pyindex \
    && pip install nvidia-nccl-cu12 \
    && pip install --no-cache-dir -r requirements.txt
