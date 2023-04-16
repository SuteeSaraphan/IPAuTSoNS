FROM python:3.6

# Install system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
      bzip2 \
      g++ \
      git \
      graphviz \
      libgl1-mesa-glx \
      libhdf5-dev \
      openmpi-bin \
      wget \
      python3-tk && \
    rm -rf /var/lib/apt/lists/*
    
# Setting up working directory 
RUN mkdir /src
WORKDIR /src

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir glob2 && \
    pip install --no-cache-dir psutil && \
    pip install --no-cache-dir tensorflow && \
    pip install --no-cache-dir keras && \
    pip install --no-cache-dir Pillow && \
    pip install --no-cache-dir opencv-python && \
    pip install --no-cache-dir torch && \
    pip install --no-cache-dir torchvision && \
    pip install --no-cache-dir torchaudio && \
    pip install --no-cache-dir matplotlib && \
    pip install --no-cache-dir pymongo[srv] && \
    pip install --no-cache-dir numpy

COPY . .
ENTRYPOINT ["python", "pixel.py"]
