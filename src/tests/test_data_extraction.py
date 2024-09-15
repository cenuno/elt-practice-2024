#!/usr/bin/python3

"""
Test custom logger module
"""

import csv
import os
from pathlib import Path

import pytest

from data_extraction import main


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
    # NOTE: call main method
    main(
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

    # NOTE: for each client and file type
    for client_name in client_names:
        for file_type in file_types:
            # NOTE: create client name and file type specific input and output dir
            input_client_file_type_dir = os.path.join(
                parent_input_dir, client_name, file_type
            )
            output_client_file_type_dir = os.path.join(
                parent_output_dir, client_name, file_type
            )
            # NOTE: for each file in the input dir, ensure it exists
            for file in os.listdir(input_client_file_type_dir):
                input_file = Path(os.path.join(input_client_file_type_dir, file))
                assert input_file.exists(), f"{input_file} does not exist"
                # NOTE: delete file
                input_file.unlink()

            # NOTE: for each file in the output dir, ensure it exists
            for file in os.listdir(output_client_file_type_dir):
                output_file = Path(os.path.join(output_client_file_type_dir, file))
                assert output_file.exists(), f"{output_file} does not exist"
                # NOTE: delete file
                output_file.unlink()


def test_main_nonexistent_client(tmp_path):
    with pytest.raises(ValueError):
        # NOTE: store variables
        input_dir = os.path.join(tmp_path, "data", "input")
        output_dir = os.path.join(tmp_path, "data", "output")
        log_output_dir = os.path.join(tmp_path, "logs")
        client_data_sources_path = Path(
            os.path.join("src", "elt_practice_2024", "client_data_sources.json")
        )
        # NOTE: call main method
        main(
            client_names=["lumi"],
            file_types=["membership", "claim"],
            input_dir=input_dir,
            output_dir=output_dir,
            sep="|",
            quoting=csv.QUOTE_NONE,
            overwrite_download=False,
            overwrite_process=False,
            log_output_dir=log_output_dir,
            client_data_sources_path=client_data_sources_path,
        )
