#!/usr/bin/python3

"""
Extract data from cloud and store it locally using ClientDataManager
"""


import csv
import os
from pathlib import Path

from custom_logger import setup_custom_logger
from client_data_manager import ClientDataManager


# NOTE: store output log dir
LOG_OUTPUT_DIR = "logs"
# NOTE: get the name of the importing script (this script)
current_script_filename = Path(os.path.basename(__file__)).stem

# NOTE: set up custom logging
logger, _ = setup_custom_logger(current_script_filename, LOG_OUTPUT_DIR)

# NOTE: store relevant client names
CLIENT_NAMES = ["acme", "hooli"]

# NOTE: store relevant file types
FILE_TYPES = []  # ["membership", "claim"]

# NOTE: store relevant CSV options
SEP = "|"
QUOTING = csv.QUOTE_NONE

# NOTE: store data dir
INPUT_DIR = os.path.join("data", "input")
OUTPUT_DIR = os.path.join("data", "output")

# NOTE: store overwrite options
OVERWRITE_DOWNLOAD = False
OVERWRITE_PROCESS = False

# NOTE: store data source path
CLIENT_DATA_SOURCES_PATH = Path("client_data_sources.json")

logger.info("for each client, download the excel files from the cloud")

for client_name in CLIENT_NAMES:
    try:
        # NOTE: init ClientDataManager with the client name and path to JSON data
        cdm = ClientDataManager(
            client_name=client_name,
            data_path=CLIENT_DATA_SOURCES_PATH,
        )
        # NOTE: download files and process them
        cdm.download_and_process_files(
            file_types=FILE_TYPES,
            input_dir=INPUT_DIR,
            output_dir=OUTPUT_DIR,
            sep=SEP,
            quoting=QUOTING,
            overwrite_download=OVERWRITE_DOWNLOAD,
            overwrite_process=OVERWRITE_PROCESS,
        )

    except ValueError as e:
        logger.warning(f"Skipping {client_name}: {e}")

logger.info("data extraction completed")
