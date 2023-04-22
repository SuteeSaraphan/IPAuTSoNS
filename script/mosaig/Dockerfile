# First stage: build
FROM python:3.6 AS builder

COPY . /app

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir pymongo[srv]

# Second stage: run
FROM python:3.6-slim

COPY --from=builder /app /app

WORKDIR /app

ENTRYPOINT ["python", "mosaig.py"]
