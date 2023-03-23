FROM nneji123/abuad-lms

WORKDIR /app

ADD . /app 

COPY templates/admin/templates /usr/local/lib/python3.8/site-packages/flask_admin/templates/bootstrap4/

RUN for i in {1..20}; do python init.py; done

CMD gunicorn -b 0.0.0.0:5000 --worker-class eventlet -w 1 app:app