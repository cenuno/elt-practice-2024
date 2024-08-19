#!/bin/bash

echo "Spinning up docker..."
sleep 1
docker compose up --detach --build --force-recreate

#echo "verify that we can now use poetry"
#sleep 1
#docker exec -it python poetry --version > haha.txt