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
        sleep 5
        python /code/manage.py exportxls
        sleep 5
    done
    python /code/manage.py email
done