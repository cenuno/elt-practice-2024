#!/usr/bin/python3

"""
Store utility functions and constants in one place for data ingestion
"""

import inspect
import os
from pathlib import Path

import psycopg2

from custom_logger import setup_function_logger
from data_extraction_utils import MetadataColumns

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


def generate_create_table_statement(
    schema_name: str,
    table_name: str,
    columns: MetadataColumns,
    conn: psycopg2.extensions.connection,
    execute: bool = True,
) -> str:
    """Generate a PostgreSQL CREATE TABLE statement from schema, table name, and column inputs

    :param schema: str - name of the schema in which the table will be created
    :param table_name: str - name of the table to be created
    :param columns: MetadataColumns -  list of dictionaries representing the column definitions.
                    Each dictionary should contain the following keys:
                        - "processed_name" (str): The column name to be used in the table.
                        - "data_type" (str): The data type of the column.
    :param conn: Connection - Handles connection to a PostgreSQL db instance & encapsulates a db session.

    :return: A string representing the formatted CREATE TABLE statement.
    """
    # NOTE: fetch function name
    function_name = inspect.currentframe().f_code.co_name  # type: ignore
    # NOTE: create function logger
    logger = setup_function_logger(
        script_name=CURRENT_SCRIPT_FILENAME, function_name=function_name
    )
    logger.info("create empty list that will store column definitions")
    column_definitions = []

    logger.info(
        "for each column, create the definition in the format: 'processed_name data_type'"
    )
    for column in columns:
        column_def = f"{column['processed_name']} {column['data_type']}"
        column_definitions.append(column_def)

    logger.info(
        "join the column definitions with commas and format it inside the CREATE TABLE statement"
    )
    column_definitions_str = ",\n    ".join(column_definitions)
    create_table_statement = f"""
    CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} (
        {column_definitions_str}
    );
    """

    if execute:
        logger.info("open a cursor to perform database operations")
        with conn:
            with conn.cursor() as curs:
                logger.info(f"query to be executed is: {create_table_statement}")
                curs.execute(create_table_statement)
                logger.info("close cursor")
                curs.close()
    else:
        logger.info("not executing the create table statement")

    return create_table_statement
