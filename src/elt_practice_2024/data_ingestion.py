#!/usr/bin/python3

"""
Ingest processed data files into PostgreSQL
"""

import os
from pathlib import Path
from typing import List, Optional

import psycopg2

from client_data_manager import ClientDataManager
from custom_logger import setup_custom_logger


def main(
    client_names: List[str],
    file_types: Optional[List[str]] = None,
    input_dir: str = os.path.join("data", "input"),
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

    logger.info("begin data ingestion")
    for client_name in client_names:
        cdm = ClientDataManager(
            client_name=client_name,
            data_path=client_data_sources_path,
        )
        logger.info(f"Processing client: {cdm.client_name}")
        logger.info(f"input dir is: {input_dir}")
        logger.info(f"file types are: {file_types}")
        logger.info("connect to postgres db")
        conn = psycopg2.connect(dsn=POSTGRES_LIBPQ_CONN_STRING)
        logger.info("open a cursor to perform database operations")
        cur = conn.cursor()
        cur.execute("SELECT usename from pg_user;")
        results = cur.fetchall()
        logger.info(f"results are: {results}")
        logger.info("close communication to database")
        cur.close()
        conn.close()

    logger.info("finished data ingestion")


if __name__ == "__main__":
    main(
        client_names=["acme", "hooli"],
        file_types=["membership", "claim"],
        input_dir=os.path.join("data", "input"),
        log_output_dir=os.path.join("logs"),
        client_data_sources_path=Path("client_data_sources.json"),
    )
