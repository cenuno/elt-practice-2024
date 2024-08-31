#!/usr/bin/python3

"""
Test ClientDataManager class
"""

import os
from pathlib import Path
import re

import pytest

from client_data_manager import ClientDataManager

# NOTE: store data source path
CLIENT_DATA_SOURCES_PATH = Path(
    os.path.join("src", "elt_practice_2024", "client_data_sources.json")
)


def test_existing_client():
    cdm = ClientDataManager(client_name="clientA", data_path=CLIENT_DATA_SOURCES_PATH)
    assert cdm.client_data is not None


def test_nonexisting_client():
    with pytest.raises(ValueError):
        ClientDataManager(client_name="clientZ", data_path=CLIENT_DATA_SOURCES_PATH)


def test_get_file_types():
    known_file_types = ["membership_files", "claim_files"]
    cdm = ClientDataManager(client_name="clientA", data_path=CLIENT_DATA_SOURCES_PATH)
    file_types = cdm.get_file_types()
    check_file_types = [file_type in known_file_types for file_type in file_types]
    assert all(check_file_types)


def test_nonexistent_file_type():
    with pytest.raises(ValueError):
        cdm = ClientDataManager(
            client_name="clientA", data_path=CLIENT_DATA_SOURCES_PATH
        )
        cdm.get_file_names(file_type="raw_data")


def test_get_membership_file_names():
    cdm = ClientDataManager(client_name="clientA", data_path=CLIENT_DATA_SOURCES_PATH)
    file_names = cdm.get_file_names(file_type="membership_files")
    check_file_names = []
    file_name_pattern = "Patient-membership-clientA-\\d{6}"
    for file_name in file_names:
        if re.fullmatch(pattern=file_name_pattern, string=file_name):
            check_file_names.append(True)
        else:
            check_file_names.append(False)
    assert all(check_file_names)


def test_get_claim_file_names():
    cdm = ClientDataManager(client_name="clientB", data_path=CLIENT_DATA_SOURCES_PATH)
    file_names = cdm.get_file_names(file_type="claim_files")
    check_file_names = []
    file_name_pattern = "Patient-claim-clientB-\\d{6}"
    for file_name in file_names:
        if re.fullmatch(pattern=file_name_pattern, string=file_name):
            check_file_names.append(True)
        else:
            check_file_names.append(False)
    assert all(check_file_names)


def test_get_file_data():
    cdm = ClientDataManager(client_name="clientB", data_path=CLIENT_DATA_SOURCES_PATH)
    file_names = cdm.get_file_names(file_type="claim_files")
    file_data = []
    # NOTE: test if relevant keys are found in this file
    for file in file_names:
        claim_file_data = cdm.get_file_data(file_type="claim_files", file_name=file)
        relevant_keys = [
            key in ["url", "excel_filename", "csv_filename"]
            for key in claim_file_data.keys()
        ]
        file_data.append(all(relevant_keys))
    # NOTE: test if all files have all relevant keys
    assert all(file_data)


def test_get_nonexisting_type_file_data():
    with pytest.raises(ValueError):
        cdm = ClientDataManager(
            client_name="clientB", data_path=CLIENT_DATA_SOURCES_PATH
        )
        cdm.get_file_data(
            file_type="awesome_claim_files", file_name="awesome_file_name"
        )


def test_get_nonexisting_name_file_data():
    with pytest.raises(ValueError):
        cdm = ClientDataManager(
            client_name="clientA", data_path=CLIENT_DATA_SOURCES_PATH
        )
        cdm.get_file_data(file_type="claim_files", file_name="awesome_file_name")


def test_get_all_filenames():
    cdm = ClientDataManager(client_name="clientA", data_path=CLIENT_DATA_SOURCES_PATH)
    excel_filenames, csv_filenames = cdm.get_all_filenames()
    check_excel_filenames = [
        ".xlsx" in excel_filename for excel_filename in excel_filenames
    ]
    check_csv_filenames = [".csv" in csv_filename for csv_filename in csv_filenames]
    assert all(check_excel_filenames) and all(check_csv_filenames)
