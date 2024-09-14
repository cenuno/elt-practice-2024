#!/usr/bin/python3
# mypy: disable-error-code="method-assign, assignment"
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
    importing_script_name: str, output_dir: str, log_level: int = int(logging.INFO)
) -> Tuple[logging.Logger, str]:
    """Create log file naming convention based on the importing script

    :param importing_script_name: str - the name of the import script
    :param output_dir: str - dir where the logs will live
    :param log_level: int - threshold for logging

    :return: logging.Logger - log object
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
    log_force = True

    # NOTE: setup logging
    logging.basicConfig(
        filename=log_filename,
        filemode=log_file_mode,
        encoding=log_encoding,
        level=log_level,
        format=log_formatter,
        force=log_force,
    )

    # Return the logger instance and the filename
    return logging.getLogger(importing_script_name), log_filename


def setup_function_logger(
    script_name: Path, function_name: str, log_level: int = int(logging.INFO)
) -> logging.Logger:
    """Create custom logger that uses the script and function name

    :param log_level: int - threshold for logging
    :return: logging.Logger - log object
    """
    logger = logging.getLogger(f"{script_name}.{function_name}")
    logger.setLevel = log_level
    return logger
