#!/usr/bin/python3

"""
Test data_ingestion_utils module
"""

import csv
import os
from pathlib import Path

import psycopg2
from psycopg2 import sql
import pytest

from client_data_manager import ClientDataManager
from data_ingestion_utils import (
    create_schema,
    drop_schema,
    create_table,
    copy_file_into_table,
)

# NOTE: fetch connection string
POSTGRES_LIBPQ_CONN_STRING = os.environ.get("POSTGRES_PYTHON_LIBPQ_CONNECTION_STRING")
# NOTE: create db connection
conn = psycopg2.connect(dsn=POSTGRES_LIBPQ_CONN_STRING)

# NOTE: store data source path
CLIENT_DATA_SOURCES_PATH = Path(
    os.path.join("src", "elt_practice_2024", "client_data_sources.json")
)


def test_create_schema():
    # NOTE: create test schema
    test_schema_name = "test_schema1"
    create_schema(schema_name=test_schema_name, conn=conn)
    query = f"""
    -- NOTE: return boolean regarding schema existence
    SELECT exists(select schema_name FROM information_schema.schemata WHERE schema_name = '{test_schema_name}');
    """
    with conn:
        with conn.cursor() as curs:
            curs.execute(query)
            # NOTE: should only ever return one record with one value
            results = curs.fetchall()[0][0]
            curs.close()
            assert results, "Schema does not exist"
    # NOTE: drop the schema and all objects
    drop_schema(schema_name=test_schema_name, conn=conn, cascade=True)


def test_drop_schema_with_cascade():
    # NOTE: create throwaway schema
    test_drop_schema_name = "test_schema2"
    create_schema(schema_name=test_drop_schema_name, conn=conn)
    table_create_query = f"""
    CREATE TABLE IF NOT EXISTS {test_drop_schema_name}.cool_table (
        id integer
    )
    """
    # NOTE: create a table
    with conn:
        with conn.cursor() as curs:
            curs.execute(table_create_query)
            curs.close()

    # NOTE: drop the schema
    drop_schema(schema_name=test_drop_schema_name, conn=conn, cascade=True)
    query = f"""
    -- NOTE: return boolean regarding schema existence
    SELECT exists(select schema_name FROM information_schema.schemata WHERE schema_name = '{test_drop_schema_name}');
    """
    with conn:
        with conn.cursor() as curs:
            curs.execute(query)
            # NOTE: should only ever return one record with one value
            results = curs.fetchall()[0][0]
            print(results)
            curs.close()
            assert not results, "Schema does exist"


def test_drop_schema_with_restrict():
    with pytest.raises(psycopg2.errors.DependentObjectsStillExist):
        # NOTE: create throwaway schema
        test_drop_schema_name = "test_schema3"
        create_schema(schema_name=test_drop_schema_name, conn=conn)
        table_create_query = f"""
        CREATE TABLE IF NOT EXISTS {test_drop_schema_name}.cool_table (
            id integer
        )
        """
        # NOTE: create a table
        with conn:
            with conn.cursor() as curs:
                curs.execute(table_create_query)
                curs.close()

        # NOTE: drop the schema
        drop_schema(schema_name=test_drop_schema_name, conn=conn, cascade=False)

    # NOTE: drop the schema and all objects
    drop_schema(schema_name=test_drop_schema_name, conn=conn, cascade=True)


def test_create_table_with_execute():
    # NOTE: store file type
    FILE_TYPE = "membership"

    # NOTE: store table name
    test_table_name = f"raw_{FILE_TYPE}_202409"
    # NOTE: create test schema
    test_schema_name = "test_schema4"
    create_schema(schema_name=test_schema_name, conn=conn)

    # NOTE: fetch relevant columns
    cdm = ClientDataManager(client_name="acme", data_path=CLIENT_DATA_SOURCES_PATH)
    metadata = cdm.get_metadata_by_file_type(file_type=FILE_TYPE)
    metadata_columns = metadata.get("columns")

    # NOTE: generate create table and execute it
    _ = create_table(
        schema_name=test_schema_name,
        table_name=test_table_name,
        columns=metadata_columns,
        conn=conn,
        execute=True,
    )

    # NOTE: confirm table exists
    query = f"""
    -- NOTE: return boolean regarding table existence
    SELECT EXISTS(
        SELECT 
            table_name 
        FROM
            information_schema.tables 
        WHERE 
            table_schema = '{test_schema_name}'
            AND table_name = '{test_table_name}'
    )
    ;
    """
    with conn:
        with conn.cursor() as curs:
            curs.execute(query)
            # NOTE: should only ever return one record with one value
            results = curs.fetchall()[0][0]
            print(results)
            curs.close()
            assert results, "Table does not exist"
    # NOTE: drop the schema and all objects
    drop_schema(schema_name=test_schema_name, conn=conn, cascade=True)


def test_create_table_without_execute():
    # NOTE: store file type
    FILE_TYPE = "membership"

    # NOTE: store table name
    test_table_name = f"raw_{FILE_TYPE}_202409"
    # NOTE: create test schema
    test_schema_name = "test_schema5"
    create_schema(schema_name=test_schema_name, conn=conn)

    # NOTE: fetch relevant columns
    cdm = ClientDataManager(client_name="acme", data_path=CLIENT_DATA_SOURCES_PATH)
    metadata = cdm.get_metadata_by_file_type(file_type=FILE_TYPE)
    metadata_columns = metadata.get("columns")

    # NOTE: generate create table and execute it
    _ = create_table(
        schema_name=test_schema_name,
        table_name=test_table_name,
        columns=metadata_columns,
        conn=conn,
        execute=False,
    )

    # NOTE: confirm table exists
    query = f"""
    -- NOTE: return boolean regarding table existence
    SELECT EXISTS(
        SELECT 
            table_name 
        FROM
            information_schema.tables 
        WHERE 
            table_schema = '{test_schema_name}'
            AND table_name = '{test_table_name}'
    )
    ;
    """
    with conn:
        with conn.cursor() as curs:
            curs.execute(query)
            # NOTE: should only ever return one record with one value
            results = curs.fetchall()[0][0]
            print(results)
            curs.close()
            assert not results, "Table does exist"
    # NOTE: drop the schema and all objects
    drop_schema(schema_name=test_schema_name, conn=conn, cascade=True)


def test_copy_file_into_table(tmp_path):
    # NOTE: create throwaway schema
    schema_name = "test_schema6"
    table_name = "cool_table"
    create_schema(schema_name=schema_name, conn=conn)
    table_create_query = f"""
    CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} (
        "id" integer
    )
    """

    # NOTE: create a table
    with conn:
        with conn.cursor() as curs:
            curs.execute(table_create_query)
            curs.close()

    # NOTE: create to write to the CSV file
    data = [["id"], [1], [2], [3]]

    # NOTE: create filename
    file_path = Path(os.path.join(tmp_path, "output.csv"))

    # NOTE: write to the CSV file
    with open(file_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)

    # NOTE: copy this file into the recently created table
    _ = copy_file_into_table(
        file_path=file_path,
        schema_name=schema_name,
        table_name=table_name,
        conn=conn,
        truncate=True,
        execute=True,
    )

    # NOTE: confirm table exists
    query = sql.SQL(
        """
    -- NOTE: return count of number of records
    SELECT 
        COUNT(1) AS num_records
    FROM
        {schema_and_table_name}
    ;
    """
    ).format(schema_and_table_name=sql.Identifier(schema_name, table_name))
    with conn:
        with conn.cursor() as curs:
            curs.execute(query)
            # NOTE: should only ever return one record with one value
            results = curs.fetchall()[0][0]
            curs.close()
            assert results > 0, "No data exists in the table"
