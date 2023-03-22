FROM python:3.8.13-slim-bullseye

WORKDIR /app

RUN apt-get -y update && apt-get install -y \
  wget \
  ffmpeg \ 
  libsm6 \
  build-essential \
  cmake \
  libxext6

RUN pip install --upgrade setuptools 

ADD ./requirements.txt /app/requirements.txt

RUN pip install dlib && pip install -r requirements.txt

ADD . /app 

RUN python init.py

CMD python app.py