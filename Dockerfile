FROM python:3.8-alpine

WORKDIR /code

# GUNICORN - not an actual dependency
RUN pip install gunicorn

RUN apk add --no-cache --update postgresql-dev python3-dev musl-dev make cmake gcc g++ gfortran \
                        libmagic zlib zlib-dev jpeg jpeg-dev libxslt libxml2 libxslt-dev libxml2-dev

# DEPENDENCIES
COPY requirements.txt .
RUN pip install -r requirements.txt && apk del make cmake gcc g++ gfortran zlib-dev jpeg-dev

COPY ampa .

EXPOSE 8000

CMD [ "/usr/local/bin/gunicorn", "ampa.wsgi:application", "--bind", "0.0.0.0:8000", "--keep-alive", "1" ]

# FROM python:3.8-slim

# WORKDIR /code

# # RUN echo "@community http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
# # RUN apk add --no-cache --update postgresql-dev python3-dev musl-dev make cmake gcc g++ gfortran \
# #                         libmagic zlib zlib-dev jpeg jpeg-dev libxslt libxml2 libxslt-dev libxml2-dev \
# #                         py3-numpy@community py3-pandas@community
# # ENV PYTHONPATH "/usr/lib/python3.8/site-packages"
# # ENV PYTHONUNBUFFERED=1
# # ENV PYTHONPATH=/usr/lib/python3.8/site-packages
# # RUN python3 -m ensurepip
# # RUN pip list && exit 1
# RUN apt-get update && apt-get install -y apt-utils libpq-dev gcc

# # GUNICORN - not an actual dependency
# RUN pip install gunicorn

# # DEPENDENCIES
# COPY requirements.txt .
# RUN pip install -r requirements.txt

# RUN apt-get clean

# COPY ampa .

# EXPOSE 8000

# CMD [ "/usr/local/bin/gunicorn", "ampa.wsgi:application", "--bind", "0.0.0.0:8000", "--keep-alive", "1" ]

