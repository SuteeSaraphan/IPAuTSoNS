FROM python:3.6

COPY . .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir pymongo[srv]


ENTRYPOINT ["python", "mosaig.py"]
