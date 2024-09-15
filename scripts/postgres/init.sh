#!/bin/bash

current_date=$(date +"%Y-%m-%d %H:%M:%S")

echo "starting at ($current_date)"
# WARNING: the password for this user is defined ahead of time within PGPASSWORD env variable
echo "create the service account user"
psql -U $POSTGRES_USER -d $POSTGRES_DB \
    -v postgres_python_user=$POSTGRES_PYTHON_USER \
    -v postgres_python_password=$POSTGRES_PYTHON_PASSWORD \
    -v postgres_python_connection_limit=$POSTGRES_PYTHON_CONNECTION_LIMIT <<< \
    "CREATE ROLE :postgres_python_user WITH LOGIN PASSWORD :'postgres_python_password' CONNECTION LIMIT :postgres_python_connection_limit;"

echo "ensure service account user can create different schemas"
psql -U $POSTGRES_USER -d $POSTGRES_DB \
    -v postgres_db=$POSTGRES_DB \
    -v postgres_python_user=$POSTGRES_PYTHON_USER <<< \
    "GRANT CREATE ON DATABASE :postgres_db TO :postgres_python_user;"

echo "all done at ($current_date)"
