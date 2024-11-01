#!/bin/bash

current_date=$(date +"%Y-%m-%d %H:%M:%S")

echo "starting at ($current_date)"
# WARNING: the password for this user is defined ahead of time within PGPASSWORD env variable
echo "create the service account user for python"
psql -U $POSTGRES_USER -d $POSTGRES_DB \
    -v postgres_python_user=$POSTGRES_PYTHON_USER \
    -v postgres_python_password=$POSTGRES_PYTHON_PASSWORD \
    -v postgres_python_connection_limit=$POSTGRES_PYTHON_CONNECTION_LIMIT <<< \
    "CREATE ROLE :postgres_python_user WITH LOGIN PASSWORD :'postgres_python_password' CONNECTION LIMIT :postgres_python_connection_limit;"

echo "ensure service account python user can create different schemas"
psql -U $POSTGRES_USER -d $POSTGRES_DB \
    -v postgres_db=$POSTGRES_DB \
    -v postgres_python_user=$POSTGRES_PYTHON_USER <<< \
    "GRANT CREATE ON DATABASE :postgres_db TO :postgres_python_user;"

echo "create the service account user for dbt"
psql -U $POSTGRES_USER -d $POSTGRES_DB \
    -v dbt_postgres_user=$DBT_POSTGRES_USER \
    -v dbt_postgres_password=$DBT_POSTGRES_PASSWORD \
    -v dbt_postgres_connection_limit=$DBT_POSTGRES_CONNECTION_LIMIT <<< \
    "CREATE ROLE :dbt_postgres_user WITH LOGIN PASSWORD :'dbt_postgres_password' CONNECTION LIMIT :dbt_postgres_connection_limit;"

echo "ensure service account dbt user has proper read permissions"
psql -U $POSTGRES_USER -d $POSTGRES_DB \
    -v postgres_db=$POSTGRES_DB \
    -v dbt_postgres_user=$DBT_POSTGRES_USER \
    -v dbt_postgres_read_role=$DBT_POSTGRES_READ_ROLE <<< \
    "GRANT :dbt_postgres_read_role TO :dbt_postgres_user;"

echo "ensure service account dbt user has proper write permissions"
psql -U $POSTGRES_USER -d $POSTGRES_DB \
    -v postgres_db=$POSTGRES_DB \
    -v dbt_postgres_user=$DBT_POSTGRES_USER \
    -v dbt_postgres_write_role=$DBT_POSTGRES_WRITE_ROLE <<< \
    "GRANT :dbt_postgres_write_role TO :dbt_postgres_user;"

echo "ensure service account dbt user can create different schemas"
psql -U $POSTGRES_USER -d $POSTGRES_DB \
    -v postgres_db=$POSTGRES_DB \
    -v dbt_postgres_user=$DBT_POSTGRES_USER <<< \
    "GRANT CREATE ON DATABASE :postgres_db TO :dbt_postgres_user;"



echo "all done at ($current_date)"
