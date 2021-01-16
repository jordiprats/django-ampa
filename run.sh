#!/bin/sh

if [ -f /code/prod.sh ];
then
    source /code/prod.sh
fi

/usr/local/bin/gunicorn ampa.wsgi:application --bind 0.0.0.0:8000 --keep-alive 1