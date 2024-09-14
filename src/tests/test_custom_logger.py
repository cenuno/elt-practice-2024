#!/usr/bin/python3

"""
Test custom logger module
"""

import inspect
import os
from pathlib import Path


from custom_logger import setup_custom_logger, setup_function_logger

# NOTE: fetch the current script name
CURRENT_SCRIPT_FILENAME = Path(os.path.basename(__file__)).stem


def test_custom_logger(tmp_path):
    # NOTE: set up custom logging
    logger, filename = setup_custom_logger(CURRENT_SCRIPT_FILENAME, tmp_path)
    logger.info("hello")
    # NOTE: fetch function name
    function_name = inspect.currentframe().f_code.co_name  # type: ignore
    # NOTE: create function logger
    logger = setup_function_logger(
        script_name=CURRENT_SCRIPT_FILENAME,
        function_name=f"{function_name}",
    )
    logger.info("goodbye")
    assert Path(filename).is_file()
