#!/usr/bin/python3

"""
Store utility functions and constants in one place for data ingestion
"""

import inspect
import os
from pathlib import Path

import psycopg2
from psycopg2 import sql

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
    logger.info("create query")
    query = sql.SQL(
        "CREATE SCHEMA IF NOT EXISTS {schema_name} AUTHORIZATION CURRENT_ROLE;"
    ).format(schema_name=sql.Identifier(schema_name))

    logger.info("open a cursor to perform database operations")
    with conn:
        with conn.cursor() as curs:
            logger.info(f"query to be executed is:\n{query.as_string(context=conn)}")
            curs.execute(query)
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
        query = sql.SQL("DROP SCHEMA IF EXISTS {schema_name} CASCADE;").format(
            schema_name=sql.Identifier(schema_name)
        )
    else:
        query = sql.SQL("DROP SCHEMA IF EXISTS {schema_name} RESTRICT;").format(
            schema_name=sql.Identifier(schema_name)
        )

    logger.info("open a cursor to perform database operations")
    with conn:
        with conn.cursor() as curs:
            logger.info(f"query to be executed is:\n{query.as_string(context=conn)}")
            curs.execute(query)
            logger.info("close cursor")
            curs.close()


def create_table(
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
    :param execute: bool - whether or not to execute the CREATE TABLE statement

    :return: A string representing the formatted CREATE TABLE statement.
    """
    # NOTE: fetch function name
    function_name = inspect.currentframe().f_code.co_name  # type: ignore
    # NOTE: create function logger
    logger = setup_function_logger(
        script_name=CURRENT_SCRIPT_FILENAME, function_name=function_name
    )
    logger.info(
        'for each column, create the definition in the format: "processed_name" data_type'
    )
    logger.info(
        "NOTE: at this time, it's not possible to blend literal and sql identifiers in the same line"
    )
    column_definitions = []
    for column in columns:
        column_definition = f"\"{column['processed_name']}\" {column['data_type']}"
        column_definitions.append(column_definition)

    logger.info(
        "join the column definitions with commas and format it inside the CREATE TABLE statement"
    )
    column_definitions_str = ",\n    ".join(column_definitions)
    query = f"""
        CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} (
            {column_definitions_str}
        )
    ;
    """

    if execute:
        logger.info("open a cursor to perform database operations")
        with conn:
            with conn.cursor() as curs:
                logger.info(f"query to be executed is:\n{query}")
                curs.execute(query)
                logger.info("close cursor")
                curs.close()

    return query


def copy_file_into_table(
    file_path: Path,
    schema_name: str,
    table_name: str,
    conn: psycopg2.extensions.connection,
    truncate: bool = True,
    execute: bool = True,
) -> str:
    """Create and execute a user composed COPY statement that reads data in and appends to a table

    :param file_path: Path - name of the file whose contents will be copied into a table
    :param schema: str - name of the schema in which the table will be created
    :param table_name: str - name of the table to be created
    :param conn: Connection - Handles connection to a PostgreSQL db instance & encapsulates a db session.
    :param truncate: bool - whether or not to delete the table before the COPY statement runs
    :param execute: bool - whether or not to execute the COPY statement

    :return: A string representing the formatted COPY statement.
    """
    # NOTE: fetch function name
    function_name = inspect.currentframe().f_code.co_name  # type: ignore
    # NOTE: create function logger
    logger = setup_function_logger(
        script_name=CURRENT_SCRIPT_FILENAME, function_name=function_name
    )
    logger.info("create schema and table name")
    schema_and_table_name = sql.Identifier(schema_name, table_name)
    if truncate:
        logger.info("remove all rows from the table")
        truncate_query = sql.SQL("TRUNCATE TABLE ONLY {schema_and_table_name};").format(
            schema_and_table_name=schema_and_table_name
        )
        logger.info("store query as string")
        truncate_query_str = truncate_query.as_string(context=conn)
        with conn:
            with conn.cursor() as curs:
                logger.info(f"query to be executed is:\n{truncate_query_str}")
                curs.execute(truncate_query)
                logger.info("close cursor")
                curs.close()

    logger.info(f"read in the given file path: {file_path}")
    with open(file_path, "r") as file:
        logger.info("create copy statement")
        query = sql.SQL(
            """
            COPY {schema_and_table_name}
            FROM STDIN
            DELIMITER '|'
            CSV HEADER
            """
        ).format(schema_and_table_name=schema_and_table_name)
        logger.info("store copy statement as string")
        query_str = query.as_string(context=conn)

        if execute:
            logger.info("open a cursor to perform database operations")
            with conn:
                with conn.cursor() as curs:
                    logger.info(f"query to be executed is:\n{query_str}")
                    curs.copy_expert(sql=query, file=file)
                    logger.info("close cursor")
                    curs.close()

    return query_str
