FROM python:3.8-alpine

WORKDIR /code

# GUNICORN - not an actual dependency
RUN pip install gunicorn

RUN apk add --no-cache --update postgresql-dev python3-dev musl-dev make cmake gcc g++ gfortran libmagic zlib zlib-dev jpeg jpeg-dev

# DEPENDENCIES
COPY requirements.txt .
RUN pip install -r requirements.txt && apk del make cmake gcc g++ gfortran zlib-dev jpeg-dev

COPY ampa .

EXPOSE 8000

CMD [ "/usr/local/bin/gunicorn", "ampa.wsgi:application", "--bind", "0.0.0.0:8000", "--keep-alive", "1" ]

