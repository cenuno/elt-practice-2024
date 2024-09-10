#!/bin/bash

current_date=$(date +"%Y-%m-%d %H:%M:%S")

echo "starting at ($current_date)"

# NOTE: create the dedicated schema
psql -U $POSTGRES_USER -d $POSTGRES_DB -v postgres_schema="$POSTGRES_SCHEMA" <<< "CREATE SCHEMA IF NOT EXISTS :postgres_schema;"

