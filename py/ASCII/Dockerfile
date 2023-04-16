FROM python:3.6

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir glob2 && \
    pip install --no-cache-dir psutil && \
    pip install --no-cache-dir Pillow && \
    pip install --no-cache-dir numpy  && \
    pip install --no-cache-dir pymongo[srv]
    

COPY ASCII.py .
ENTRYPOINT ["python", "ASCII.py"]
