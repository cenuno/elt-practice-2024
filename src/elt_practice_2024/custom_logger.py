#!/usr/bin/python3

"""
Create custom logging logic
"""

import logging
import os
from pathlib import Path
from typing import Tuple

import pendulum


# NOTE:
def setup_custom_logger(
    importing_script_name: str, output_dir: str
) -> Tuple[logging.Logger, str]:
    """Create log file naming convention based on the importing script

    :param importing_script_name: str - the name of the import script
    :param output_dir: str - dir where the logs will live

    :return: logging.getLoggerClass - root logger
    """
    log_now_timestamp = pendulum.now().to_iso8601_string()
    log_filename = os.path.join(
        output_dir, f"{log_now_timestamp}_{importing_script_name}.log"
    )

    # NOTE: make the directory of the log file
    Path(os.path.dirname(log_filename)).mkdir(parents=True, exist_ok=True)

    # NOTE: set log configurations
    log_encoding = "utf-8"
    log_file_mode = "w"
    log_formatter = "%(asctime)s %(name)12s %(levelname)8s %(message)s"
    log_force = False

    # NOTE: setup logging
    logging.basicConfig(
        filename=log_filename,
        filemode=log_file_mode,
        encoding=log_encoding,
        level=logging.DEBUG,
        format=log_formatter,
        force=log_force,
    )

    # Return the logger instance and the filename
    return logging.getLogger(__name__), log_filename
