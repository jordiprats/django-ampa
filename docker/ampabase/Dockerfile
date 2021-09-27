FROM python:3.8-alpine

WORKDIR /code

# GUNICORN - not an actual dependency
RUN pip install gunicorn

RUN apk add --no-cache --update postgresql-dev python3-dev musl-dev make cmake gcc g++ gfortran \
                        libmagic zlib zlib-dev jpeg jpeg-dev libxslt libxml2 libxslt-dev libxml2-dev

# DEPENDENCIES
COPY requirements.txt .
RUN pip install -r requirements.txt && apk del make cmake gcc g++ gfortran zlib-dev jpeg-dev libxslt-dev libxml2-dev