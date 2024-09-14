#!/usr/bin/python3

"""
Extract data from cloud and store it locally using ClientDataManager
"""

import csv
import os
from pathlib import Path
from typing import List, Optional

from custom_logger import setup_custom_logger
from client_data_manager import ClientDataManager


def main(
    client_names: List[str],
    file_types: Optional[List[str]] = None,
    input_dir: str = os.path.join("data", "input"),
    output_dir: str = os.path.join("data", "output"),
    sep: str = "|",
    quoting: int = csv.QUOTE_NONE,
    overwrite_download: bool = False,
    overwrite_process: bool = False,
    log_output_dir: str = os.path.join("logs"),
    client_data_sources_path: Path = Path("client_data_sources.json"),
) -> None:
    """
    Main method to extract data for clients and store it locally.

    :param client_names: List[str] - List of client names to process
    :param file_types: Optional[List[str]] - List of file types to process. If None, all types are processed
    :param input_dir: str - Directory to download files to
    :param output_dir: str - Directory to store processed files
    :param sep: str - Delimiter used in CSV files
    :param quoting: int - CSV quoting option
    :param overwrite_download: bool - Flag to overwrite downloaded files
    :param overwrite_process: bool - Flag to overwrite processed files
    :param log_output_dir: str - Directory for storing logs
    :param client_data_sources_path: str - Path to client data sources JSON
    :param current_script_filename: Optional[str] - Name of the current script for logging purposes
    """

    # NOTE: use current script name
    current_script_filename = Path(os.path.basename(__file__)).stem

    # NOTE: set up custom logging
    logger, _ = setup_custom_logger(current_script_filename, log_output_dir)

    # NOTE: init ClientDataManager and process files for each client
    logger.info("Starting data extraction for clients")

    for client_name in client_names:
        logger.info(f"Processing client: {client_name}")
        cdm = ClientDataManager(
            client_name=client_name,
            data_path=Path(client_data_sources_path),
        )

        # Download and process files
        cdm.download_and_process_files(
            file_types=file_types,
            input_dir=input_dir,
            output_dir=output_dir,
            sep=sep,
            quoting=quoting,
            overwrite_download=overwrite_download,
            overwrite_process=overwrite_process,
        )

    logger.info("Data extraction completed")


if __name__ == "__main__":
    main(
        client_names=["acme", "hooli"],
        file_types=["membership", "claim"],
        input_dir="data/input",
        output_dir="data/output",
        sep="|",
        quoting=csv.QUOTE_NONE,
        overwrite_download=False,
        overwrite_process=False,
        log_output_dir="logs",
        client_data_sources_path=Path("client_data_sources.json"),
    )
