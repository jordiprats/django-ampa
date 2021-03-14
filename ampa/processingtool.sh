#!/bin/sh

#             FREQUENCIES
#            =============
# import/export:    cada 5 segons aprox
# email:            cada 5 minuts aprox

while true
do
    for i in $(seq 1 30);
    do
        python /code/manage.py importxls
        sleep 2
        python /code/manage.py exportxls
        sleep 2
        python /code/manage.py exportjuntapdf
        sleep 3
    done
    python /code/manage.py sendmailing
done