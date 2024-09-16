#!/usr/bin/python3

"""
Test data_ingestion_utils module
"""

import os
from pathlib import Path

import psycopg2
import pytest

from client_data_manager import ClientDataManager
from data_ingestion_utils import (
    create_schema,
    drop_schema,
    generate_create_table_statement,
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


def test_generate_create_table_statement_with_execute():
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
    _ = generate_create_table_statement(
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


def test_generate_create_table_statement_without_execute():
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
    _ = generate_create_table_statement(
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
