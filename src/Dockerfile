FROM nneji123/abuad-lms

WORKDIR /app

ADD . /app 

COPY /templates/admin/templates /usr/local/lib/python3.8/site-packages/flask_admin/templates/bootstrap4/admin/

RUN pip install tqdm

RUN ./init.sh

CMD gunicorn -b 0.0.0.0:5000 --worker-class eventlet -w 1 app:app