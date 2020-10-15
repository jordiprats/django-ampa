#!/bin/bash

while true
do
    docker exec -dt 3073f89fb0bd python /code/manage.py importxls
    sleep 5
done