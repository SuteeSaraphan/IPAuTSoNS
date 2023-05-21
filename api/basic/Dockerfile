# Stage 1: Build stage
FROM python:3.9-slim-buster AS build

RUN apt-get update && \
    apt-get install -y build-essential && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --user --no-cache-dir --upgrade pip && \
    pip install --user --no-cache-dir --requirement requirements.txt

COPY . .

# Stage 2: Runtime stage
FROM tiangolo/uvicorn-gunicorn:python3.9-slim

LABEL maintainer="team-erc"

ENV WORKERS_PER_CORE=4 
ENV MAX_WORKERS=24
ENV LOG_LEVEL="warning"
ENV TIMEOUT="200"

WORKDIR /app

COPY --from=build /root/.local /root/.local

COPY . .

EXPOSE 4020

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4020"]
