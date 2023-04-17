# Build stage
FROM python:3.6-slim AS build

RUN apt-get update && \
    apt-get install -y build-essential && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir glob2 && \
    pip install --no-cache-dir psutil && \
    pip install --no-cache-dir Pillow && \
    pip install --no-cache-dir numpy && \
    pip install --no-cache-dir pymongo[srv]

# Final stage
FROM python:3.6-slim

WORKDIR /app

COPY --from=build /usr/local/lib/python3.6/site-packages /usr/local/lib/python3.6/site-packages
COPY ASCII.py .

CMD ["python", "ASCII.py"]
