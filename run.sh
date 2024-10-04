#!/bin/bash

echo "Spinning up docker..."
sleep 1
docker compose up --detach --build --force-recreate --remove-orphans postgres pgadmin python nginx
echo "Extract data from cloud..."
docker exec -w /elt-practice-2024/src/elt_practice_2024 python python data_extraction.py
sleep 1

echo "Ingest data into postgres..."
docker exec -w /elt-practice-2024/src/elt_practice_2024 python python data_ingestion.py
sleep 1

echo "Install dbt dependencies..."
docker exec -w /elt-practice-2024/src/elt_dbt python dbt deps

echo "Run DBT models..."
docker exec -w /elt-practice-2024/src/elt_dbt python dbt run

echo "Generate DBT docs..."
docker exec -w /elt-practice-2024/src/elt_dbt python dbt docs generate

# echo "Serve DBT docs..."
# docker exec -w /elt-practice-2024/src/elt_dbt python dbt docs serve

echo "All done!"
