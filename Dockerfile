# FROM python:3.12.5-slim-buster

# WORKDIR /app

# COPY . /app

# RUN pip install -r requirements.txt

# CMD [ "python3","app.py" ]


FROM python:3.13.3-alpine

# Set working directory
WORKDIR /app

# Copy source code
COPY . .

# Install build tools and dependencies for common Python packages
RUN apk add --no-cache \
    build-base \
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
    && pip install --no-cache-dir -r requirements.txt

# Command to run the app
CMD ["python3", "app.py"]