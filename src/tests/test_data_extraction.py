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
    input_dir = os.path.join(tmp_path, "data", "input")
    output_dir = os.path.join(tmp_path, "data", "output")
    log_output_dir = os.path.join(tmp_path, "logs")
    client_data_sources_path = Path(
        os.path.join("src", "elt_practice_2024", "client_data_sources.json")
    )
    # NOTE: call main method
    main(
        client_names=["acme", "hooli"],
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

    # NOTE: store files from input dir and output dir
    input_dir_files = [
        Path(os.path.join(input_dir, file)) for file in os.listdir(input_dir)
    ]
    output_dir_files = [
        Path(os.path.join(output_dir, file)) for file in os.listdir(output_dir)
    ]

    assert len(input_dir_files) > 0, "no input files were downloaded"
    assert len(output_dir_files) > 0, "no output files were processed"

    # NOTE: ensure each file was truly created
    for input_file, output_file in zip(input_dir_files, output_dir_files):
        assert input_file.is_file(), f"{input_file} does not exist"
        assert output_file.is_file(), f"{output_file} does not exist"
        # NOTE: delete files so that we don't have to worry about it
        input_file.unlink()
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
