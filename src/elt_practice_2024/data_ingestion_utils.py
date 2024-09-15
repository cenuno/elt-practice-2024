#!/usr/bin/python3

"""
Store utility functions and constants in one place for data ingestion
"""

import inspect
import os
from pathlib import Path

import psycopg2

from custom_logger import setup_function_logger

# NOTE: store constants
CURRENT_SCRIPT_FILENAME = Path(os.path.basename(__file__)).stem


def create_schema(
    schema_name: str,
    conn: psycopg2.extensions.connection,
) -> None:
    """Create a schema if it does not exist

    :param schema_name: str - name of schema
    :param conn: Connection - Handles connection to a PostgreSQL db instance & encapsulates a db session.
    :return: None
    """
    # NOTE: fetch function name
    function_name = inspect.currentframe().f_code.co_name  # type: ignore
    # NOTE: create function logger
    logger = setup_function_logger(
        script_name=CURRENT_SCRIPT_FILENAME, function_name=function_name
    )
    logger.info("create template schema query")
    schema_query = f"""
    CREATE SCHEMA IF NOT EXISTS {schema_name} AUTHORIZATION CURRENT_ROLE;
    """

    logger.info("open a cursor to perform database operations")
    with conn:
        with conn.cursor() as curs:
            logger.info(f"query to be executed is: {schema_query}")
            curs.execute(schema_query)
            logger.info("close cursor")
            curs.close()


def drop_schema(
    schema_name: str,
    conn: psycopg2.extensions.connection,
    cascade: bool = True,
) -> None:
    """Drop a schema

    :param schema_name: str - name of schema
    :param conn: Connection - Handles connection to a PostgreSQL db instance & encapsulates a db session.
    :param cascade: bool - drop objects within the schema and any dependency objects outside of schema
    :return: None
    """
    # NOTE: fetch function name
    function_name = inspect.currentframe().f_code.co_name  # type: ignore
    # NOTE: create function logger
    logger = setup_function_logger(
        script_name=CURRENT_SCRIPT_FILENAME, function_name=function_name
    )
    logger.info("create template schema query")
    if cascade:
        schema_query = f"""
        DROP SCHEMA IF EXISTS {schema_name} CASCADE;
        """
    else:
        schema_query = f"""
        DROP SCHEMA IF EXISTS {schema_name} RESTRICT;
        """

    logger.info("open a cursor to perform database operations")
    with conn:
        with conn.cursor() as curs:
            logger.info(f"query to be executed is: {schema_query}")
            curs.execute(schema_query)
            logger.info("close cursor")
            curs.close()
