#!/usr/bin/python3

"""
Test data_ingestion_utils module
"""
import os

import psycopg2
import pytest

from data_ingestion_utils import create_schema, drop_schema

# NOTE: fetch connection string
POSTGRES_LIBPQ_CONN_STRING = os.environ.get("POSTGRES_PYTHON_LIBPQ_CONNECTION_STRING")
# NOTE: create db connection
conn = psycopg2.connect(dsn=POSTGRES_LIBPQ_CONN_STRING)


def test_create_schema():
    # NOTE: create test schema
    test_schema_name = "test_schema"
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
    drop_schema(schema_name=test_schema_name, conn=conn, cascade=True)


def test_drop_schema_with_cascade():
    # NOTE: create throwaway schema
    test_drop_schema_name = "test_drop_schema"
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
        test_drop_schema_name = "test_drop_schema2"
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

    drop_schema(schema_name=test_drop_schema_name, conn=conn, cascade=True)
