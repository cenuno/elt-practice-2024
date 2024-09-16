#!/usr/bin/python3

"""
Ingest processed data files into PostgreSQL
"""

import os
from pathlib import Path
from typing import List

import psycopg2

from client_data_manager import ClientDataManager
from custom_logger import setup_custom_logger
from data_ingestion_utils import (
    create_schema,
    generate_create_table_statement,
)


def main(
    client_names: List[str],
    file_types: List[str],
    input_dir: str = os.path.join("data", "output"),
    log_output_dir: str = os.path.join("logs"),
    client_data_sources_path: Path = Path("client_data_sources.json"),
) -> None:
    """
    Main method to ingest data into the database

    :param client_names: List[str] - List of client names to process
    :param file_types: Optional[List[str]] - List of file types to process. If None, all types are processed
    :param input_dir: str - parent directory where processed files live
    :param log_output_dir: str - Directory for storing logs
    :param client_data_sources_path: Path - Path to client data sources JSON
    """
    # NOTE: use current script name
    current_script_filename = Path(os.path.basename(__file__)).stem

    # NOTE: set up custom logging
    logger, _ = setup_custom_logger(current_script_filename, log_output_dir)

    # NOTE: init ClientDataManager and process files for each client
    logger.info("Starting data ingestion for clients")

    # NOTE: fetch constants
    logger.info("fetch posgres libpq connection string from .env")
    POSTGRES_LIBPQ_CONN_STRING = os.environ.get(
        "POSTGRES_PYTHON_LIBPQ_CONNECTION_STRING"
    )

    logger.info("connect to db")
    conn = psycopg2.connect(dsn=POSTGRES_LIBPQ_CONN_STRING)

    logger.info("begin data ingestion")
    for client_name in client_names:
        cdm = ClientDataManager(
            client_name=client_name,
            data_path=client_data_sources_path,
        )
        logger.info(f"processing client: {cdm.client_name}")
        client_dir = os.path.join(input_dir, cdm.client_name)
        logger.info(f"input dir is: {input_dir}")
        logger.info(f"file types are: {file_types}")
        logger.info("create a client specific schema if it does not exist")
        schema_name = f"client_{cdm.client_name}"
        create_schema(schema_name=schema_name, conn=conn)

        logger.info("for each input file, create a specific table")
        for file_type in file_types:
            logger.info(f"fetch metadata for this file type: {file_type}")
            metadata = cdm.get_metadata_by_file_type(file_type=file_type)
            metadata_columns = metadata.get("columns")
            file_type_dir = os.path.join(client_dir, file_type)
            for file in os.listdir(file_type_dir):
                logger.info(f"use {file} as table name without the .csv extension")
                table_name = file.replace(".csv", "")
                _ = generate_create_table_statement(
                    schema_name=schema_name,
                    table_name=table_name,
                    columns=metadata_columns,
                    conn=conn,
                    execute=True,
                )

    logger.info("close connection to db")
    conn.close()
    logger.info("finished data ingestion")


if __name__ == "__main__":
    main(
        client_names=["acme", "hooli"],
        file_types=["membership", "claim"],
        input_dir=os.path.join("data", "output"),
        log_output_dir=os.path.join("logs"),
        client_data_sources_path=Path("client_data_sources.json"),
    )
