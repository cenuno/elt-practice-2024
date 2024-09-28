#!/bin/bash

echo "Spinning up docker..."
sleep 1
docker compose up --detach --build --force-recreate --remove-orphans

echo "Extract data from cloud..."
docker exec -w /elt-practice-2024/src/elt_practice_2024 python python data_extraction.py
sleep 1

echo "Ingest data into postgres..."
docker exec -w /elt-practice-2024/src/elt_practice_2024 python python data_ingestion.py
sleep 1

echo "All done!"
#echo "verify that we can now use poetry"
#sleep 1
#docker exec -it python poetry --version > haha.txt