# Build stage
FROM python:3.6 AS build

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.6-slim

WORKDIR /app

COPY --from=build requirements.txt .
COPY . .

CMD ["python", "pixel.py"]