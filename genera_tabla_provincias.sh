#!/bin/bash
OIFS=$IFS  
IFS=$'\n'
for provincia in `cat provincias.txt`
do
    json="{\"provincia\" : \"$provincia\"}"
    echo "$json"
    curl --dump-header - -H "Content-Type: application/json" -X POST --data "$json" http://localhost:8000/api/v1/provincias/
    sleep 0.2
done
IFS=$OIFS
