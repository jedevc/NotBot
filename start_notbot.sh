#!/bin/bash

if [ $# -eq 0 ]
    then
        echo "No arguments supplied"
        exit
fi

while [ 1 ]
do
    python3 source/main.py $1 $2
    sleep 10
done
