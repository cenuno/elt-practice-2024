#!/usr/bin/python3

"""
Test the main data ingestion module
"""

import csv
import os
from pathlib import Path

import pytest

from data_extraction import main as data_extraction_main
from data_ingestion import main


def test_main_custom_params(tmp_path):
    # NOTE: store variables
    client_names = ["acme", "hooli"]
    file_types = ["membership", "claim"]
    parent_input_dir = os.path.join(tmp_path, "data", "input")
    parent_output_dir = os.path.join(tmp_path, "data", "output")
    log_output_dir = os.path.join(tmp_path, "logs")
    client_data_sources_path = Path(
        os.path.join("src", "elt_practice_2024", "client_data_sources.json")
    )
    # NOTE: call main data extractionmethod
    data_extraction_main(
        client_names=client_names,
        file_types=file_types,
        input_dir=parent_input_dir,
        output_dir=parent_output_dir,
        sep="|",
        quoting=csv.QUOTE_NONE,
        overwrite_download=False,
        overwrite_process=False,
        log_output_dir=log_output_dir,
        client_data_sources_path=client_data_sources_path,
    )
    try:
        main(
            client_names=client_names,
            file_types=file_types,
            source_dir=parent_output_dir,
            log_output_dir=log_output_dir,
            client_data_sources_path=client_data_sources_path,
        )
    except Exception as e:
        pytest.fail(f"Unexpected error: {e}")
