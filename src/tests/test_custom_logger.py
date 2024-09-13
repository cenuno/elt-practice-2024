import logging
import os
from pathlib import Path

import pendulum

from custom_logger import setup_custom_logger


def test_setup_custom_logger_creates_log_file(tmp_path):
    # Given
    importing_script_name = Path(os.path.basename(__file__)).stem
    output_dir = tmp_path  # Use pytest's tmp_path for temporary directory
    expected_log_prefix = (
        pendulum.now().to_iso8601_string().split("T")[0]
    )  # Only match date part

    # When
    logger, log_filename = setup_custom_logger(importing_script_name, str(output_dir))
    logger.info("hello world")
    # Then
    # 1. Check the logger instance
    assert isinstance(logger, logging.getLoggerClass())

    # 2. Check if the log file is created
    log_file_path = Path(log_filename)
    assert log_file_path.exists(), f"Expected log file {log_file_path} to be created"

    # 3. Check if the log filename matches the expected pattern
    assert log_file_path.name.startswith(
        expected_log_prefix
    ), f"Expected log file to start with '{expected_log_prefix}', but got {log_file_path.name}"
    assert log_file_path.name.endswith(
        f"_{importing_script_name}.log"
    ), f"Expected log file to end with '_{importing_script_name}.log', but got {log_file_path.name}"

    # 4. Check if logger is writing to the correct file
    test_message = "This is a test log message"
    logger.info(test_message)

    # Flush the logger to ensure the message is written
    for handler in logger.handlers:
        handler.flush()

    # Read the log file and verify the content
    with log_file_path.open("r", encoding="utf-8") as log_file:
        log_content = log_file.read()
        assert (
            test_message in log_content
        ), f"Log content does not contain expected message: {test_message}"
