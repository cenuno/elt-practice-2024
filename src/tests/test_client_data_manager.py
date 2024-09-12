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


def test_get_membership_file_names():
    cdm = ClientDataManager(client_name="acme", data_path=CLIENT_DATA_SOURCES_PATH)
    files = cdm.get_all_filenames()
    internal_filenames = files["membership"]["internal_filenames"]
    check_internal_file_names = []
    # NOTE: using an f-string here seemed like a non-starter
    file_name_pattern = "processed_acme_patient_membership_\\d{6}.csv"
    for file_name in internal_filenames:
        if re.fullmatch(pattern=file_name_pattern, string=str(file_name)):
            check_internal_file_names.append(True)
        else:
            check_internal_file_names.append(False)

    assert all(check_internal_file_names)


def test_get_claim_file_names():
    cdm = ClientDataManager(client_name="hooli", data_path=CLIENT_DATA_SOURCES_PATH)
    files = cdm.get_all_filenames()
    internal_filenames = files["claim"]["internal_filenames"]
    check_internal_file_names = []
    # NOTE: using an f-string here seemed like a non-starter
    file_name_pattern = "processed_hooli_patient_claim_\\d{6}.csv"
    for file_name in internal_filenames:
        if re.fullmatch(pattern=file_name_pattern, string=str(file_name)):
            check_internal_file_names.append(True)
        else:
            check_internal_file_names.append(False)

    assert all(check_internal_file_names)


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
