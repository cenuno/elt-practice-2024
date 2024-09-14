#!/usr/bin/python3

"""
Test ClientDataManager class
"""

import csv
import os
from pathlib import Path

import pytest

from client_data_manager import ClientDataManager

# NOTE: store data source path
CLIENT_DATA_SOURCES_PATH = Path(
    os.path.join("src", "elt_practice_2024", "client_data_sources.json")
)


def test_existing_client():
    cdm = ClientDataManager(client_name="acme", data_path=CLIENT_DATA_SOURCES_PATH)
    assert cdm.client_data is not None


def test_nonexisting_client():
    with pytest.raises(ValueError):
        ClientDataManager(client_name="clientZ", data_path=CLIENT_DATA_SOURCES_PATH)


def test_get_file_types():
    known_file_types = ["membership", "claim"]
    cdm = ClientDataManager(client_name="acme", data_path=CLIENT_DATA_SOURCES_PATH)
    file_types = cdm.get_file_types()
    check_file_types = [file_type in known_file_types for file_type in file_types]
    assert all(check_file_types)


def test_nonexistent_file_type():
    with pytest.raises(ValueError):
        cdm = ClientDataManager(client_name="acme", data_path=CLIENT_DATA_SOURCES_PATH)
        cdm.get_files_by_type(file_type="raw_data")


def test_get_metdata_by_file_type():
    cdm = ClientDataManager(client_name="hooli", data_path=CLIENT_DATA_SOURCES_PATH)
    membership_metadata = cdm.get_metadata_by_file_type(file_type="membership")
    key_check = []
    for key in ["columns", "schema_name", "table_name"]:
        if key in membership_metadata.keys():
            key_check.append(True)
        else:
            key_check.append(False)
    assert all(key_check)


def test_nonexistent_metadata_file_type():
    with pytest.raises(ValueError):
        cdm = ClientDataManager(client_name="hooli", data_path=CLIENT_DATA_SOURCES_PATH)
        cdm.get_metadata_by_file_type(file_type="raw_data")


def test_download_and_process_known_file_types(tmp_path):
    # NOTE: store relevant file types
    FILE_TYPES = ["membership", "claim"]

    # NOTE: store relevant CSV options
    SEP = "|"
    QUOTING = csv.QUOTE_NONE

    # NOTE: store data dir
    INPUT_DIR = os.path.join(tmp_path, "input")
    OUTPUT_DIR = os.path.join(tmp_path, "output")

    # NOTE: store overwrite options
    OVERWRITE_DOWNLOAD = True
    OVERWRITE_PROCESS = True

    # NOTE: init ClientDataManager with the client name and path to JSON data
    cdm = ClientDataManager(client_name="hooli", data_path=CLIENT_DATA_SOURCES_PATH)

    # NOTE: fetch the input files
    input_files = []
    output_files = []
    for file_type in FILE_TYPES:
        files = cdm.get_files_by_type(file_type=file_type)
        for file in files:
            # NOTE: store relative paths
            input_file_path = Path(os.path.join(INPUT_DIR, file["external_filename"]))
            output_file_path = Path(os.path.join(OUTPUT_DIR, file["internal_filename"]))
            input_files.append(input_file_path)
            output_files.append(output_file_path)

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

    # NOTE: for each file, determine that it exists
    check_input_files = [input_file.is_file() for input_file in input_files]
    check_output_files = [output_file.is_file() for output_file in output_files]

    assert all(check_input_files), "Not all input files were found"
    assert all(check_output_files), "Not all output files were found"


def test_download_and_process_unknown_file_types(tmp_path):
    with pytest.raises(ValueError):
        # NOTE: init ClientDataManager with the client name and path to JSON data
        cdm = ClientDataManager(client_name="hooli", data_path=CLIENT_DATA_SOURCES_PATH)

        # NOTE: store relevant file types
        FILE_TYPES = ["members", "claims"]

        # NOTE: store relevant CSV options
        SEP = "|"
        QUOTING = csv.QUOTE_NONE

        # NOTE: store data dir
        INPUT_DIR = os.path.join(tmp_path, "input2")
        OUTPUT_DIR = os.path.join(tmp_path, "output2")

        # NOTE: store overwrite options
        OVERWRITE_DOWNLOAD = True
        OVERWRITE_PROCESS = True

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


def test_download_and_process_all_file(tmp_path):
    # NOTE: store relevant file types
    FILE_TYPES = ["membership", "claim"]

    # NOTE: store relevant CSV options
    SEP = "|"
    QUOTING = csv.QUOTE_NONE

    # NOTE: store data dir
    INPUT_DIR = os.path.join(tmp_path, "input3")
    OUTPUT_DIR = os.path.join(tmp_path, "output3")

    # NOTE: store overwrite options
    OVERWRITE_DOWNLOAD = False
    OVERWRITE_PROCESS = False

    # NOTE: init ClientDataManager with the client name and path to JSON data
    cdm = ClientDataManager(client_name="acme", data_path=CLIENT_DATA_SOURCES_PATH)

    # NOTE: fetch the input files
    input_files = []
    output_files = []
    for file_type in FILE_TYPES:
        files = cdm.get_files_by_type(file_type=file_type)
        for file in files:
            # NOTE: store relative paths
            input_file_path = Path(os.path.join(INPUT_DIR, file["external_filename"]))
            output_file_path = Path(os.path.join(OUTPUT_DIR, file["internal_filename"]))
            input_files.append(input_file_path)
            output_files.append(output_file_path)

    # NOTE: download files and process them
    cdm.download_and_process_files(
        file_types=[],
        input_dir=INPUT_DIR,
        output_dir=OUTPUT_DIR,
        sep=SEP,
        quoting=QUOTING,
        overwrite_download=OVERWRITE_DOWNLOAD,
        overwrite_process=OVERWRITE_PROCESS,
    )

    # NOTE: for each file, determine that it exists
    check_input_files = [input_file.is_file() for input_file in input_files]
    check_output_files = [output_file.is_file() for output_file in output_files]
    print(input_files, check_input_files, output_files, check_output_files)

    assert all(check_input_files), "Not all input files were found"
    assert all(check_output_files), "Not all output files were found"
