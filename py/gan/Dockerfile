# Stage 1: Build the Python dependencies
FROM python:3.6-slim as builder

COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --user --no-cache-dir --upgrade pip && \
    pip install --user --no-cache-dir --requirement requirements.txt

# Stage 2: Build the final image
FROM python:3.6-slim

COPY --from=builder /usr/local/lib/python3.6/site-packages /usr/local/lib/python3.6/site-packages

COPY . .

ENTRYPOINT ["python", "main.py"]
