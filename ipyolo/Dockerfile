# Stage 1: Build stage
FROM python:3.9-slim as build

LABEL maintainer="team-erc"

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --user --no-cache-dir --upgrade pip \
    && pip install --user --no-cache-dir --requirement requirements.txt

# Stage 2: Runtime stage
FROM tiangolo/uvicorn-gunicorn:python3.9-slim

ENV WORKERS_PER_CORE=4 
ENV MAX_WORKERS=24
ENV LOG_LEVEL="warning"
ENV TIMEOUT="200"

COPY --from=build /root/.local /root/.local

COPY . /app

WORKDIR /app

EXPOSE 4050

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4050"]
