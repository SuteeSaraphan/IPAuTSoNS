FROM python:3.6 AS build

RUN apt-get update && \
    apt-get install -y build-essential && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir pymongo[srv] && \
    pip install --no-cache-dir --no-build-isolation opencv-python-headless

COPY . .


# Second stage: run
FROM python:3.6-slim

WORKDIR /app

COPY --from=build /usr/local/lib/python3.6/site-packages /usr/local/lib/python3.6/site-packages

COPY . .

ENTRYPOINT ["python", "mosaig.py"]
