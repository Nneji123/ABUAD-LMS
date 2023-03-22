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

COPY requirements.txt .

RUN pip install dlib && pip install -r requirements.txt

ADD . . 

RUN cd src && python init.py

CMD python app.py