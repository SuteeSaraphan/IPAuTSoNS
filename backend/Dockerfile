FROM --platform=$BUILDPLATFORM python:3.10-slim-buster AS backend


RUN mkdir /backend

WORKDIR /backend

COPY req.txt /backend

RUN apt update

RUN apt install gcc -y

RUN pip3 install -U setuptools

RUN pip3 install --upgrade pip

RUN pip3 install -r req.txt 

RUN pip3 install pymongo[srv]

COPY . /backend


WORKDIR /backend/IPAutSoNsAPI

ENTRYPOINT ["python3"] 

CMD ["manage.py", "runserver", "0.0.0.0:8000"]

