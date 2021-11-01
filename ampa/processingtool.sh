#!/bin/sh

#             FREQUENCIES
#            =============
# import/export:    cada 5 segons aprox
# email:            cada 5 minuts aprox

echo "AMPA app version: ${AMPA_APP_VERSION}"

echo "Processing tool - sleeping for 1 minute to startup"

sleep 1m

python /code/manage.py migrate

echo "Processing tool - starting loop"

while true
do
    for i in $(seq 1 30);
    do
        echo "Processing iteration $i/30"
        python /code/manage.py importxls
        sleep 2
        python /code/manage.py exportxls
        sleep 2
        python /code/manage.py exportjuntapdf
        sleep 3
    done
    echo "Checking for mailings..."
    python /code/manage.py sendmailing
done