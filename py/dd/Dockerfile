FROM python:3.9-slim

LABEL maintainer="team-erc"

ENV WORKERS_PER_CORE=4 
ENV MAX_WORKERS=24
ENV LOG_LEVEL="warning"
ENV TIMEOUT="200"

RUN mkdir /binAPI

COPY requirements.txt /binAPI/

COPY . /binAPI/

WORKDIR /binAPI

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /var/cache/apt/* /tmp/* /var/tmp/*

EXPOSE 4020

CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "4020"]
