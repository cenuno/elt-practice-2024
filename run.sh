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

echo "Clean out any existing DBT target folders..."
docker compose run --rm dbt clean

echo "Install DBT dependencies..."
docker compose run --rm dbt deps

echo "Ensure all DBT files can be parsed..."
docker compose run --rm dbt parse

echo "Build DBT models..."
docker compose run --rm dbt build

echo "Generate DBT docs..."
docker compose run --rm dbt docs generate

echo "Spin up ngnix..."
docker run -d -p 3000:80 dbt-docs-nginx

echo "Copy DBT doc files into nginx..."
docker cp ./src/elt_dbt/target/. nginx:/usr/share/nginx/html

echo "You can now view DBT docs at http://localhost:3000/#!/overview. Enjoy the data lineage!"

echo "All done!"
