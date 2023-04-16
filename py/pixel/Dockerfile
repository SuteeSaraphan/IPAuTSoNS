FROM python:3.6


RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir glob2 && \
    pip install --no-cache-dir psutil && \
    pip install --no-cache-dir tensorflow && \
    pip install --no-cache-dir keras && \
    pip install --no-cache-dir Pillow && \
    pip install --no-cache-dir torch && \
    pip install --no-cache-dir torchvision && \
    pip install --no-cache-dir torchaudio && \
    pip install --no-cache-dir matplotlib && \
    pip install --no-cache-dir pymongo[srv] && \
    pip install --no-cache-dir numpy

COPY . .
ENTRYPOINT ["python", "pixel.py"]
