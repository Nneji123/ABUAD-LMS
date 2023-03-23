FROM nneji123/abuad-lms

WORKDIR /app

# RUN apt-get -y update && apt-get install -y \
#   wget \
#   ffmpeg \ 
#   libsm6 \
#   build-essential \
#   cmake \
#   libxext6

# RUN pip install --upgrade setuptools 

# ADD ./requirements.txt /app/requirements.txt

ADD . /app 

RUN for i in {1..20}; do python init.py; done

CMD gunicorn -b 0.0.0.0:5000 --worker-class eventlet -w 1 app:app