#!/bin/sh

if [ -f /code/prod.sh ];
then
    source /code/prod.sh
fi

python /code/manage.py migrate

/usr/local/bin/gunicorn ampa.wsgi:application --bind 0.0.0.0:8000 --keep-alive 1