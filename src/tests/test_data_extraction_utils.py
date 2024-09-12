#!/usr/bin/python3

"""
Test methods from data_extraction_utils 
"""

import os
from pathlib import Path
from unittest import mock

import pandas as pd
import pytest

from data_extraction_utils import download_file, remove_non_printable_chars, process_csv

# Mock constants for pendulum timezone and other constants if needed
TIMEZONE = "UTC"


@pytest.fixture
def setup_files(tmp_path):
    # Setup temporary files for testing
    external_filename = tmp_path / "test_input.csv"
    internal_filename = tmp_path / "test_output.csv"

    # Create a sample input CSV file
    df = pd.DataFrame(
        {
            "member_id": ["001", "002"],
            "member_last_name": ["Smith", "Doe"],
            "gender": ["M", "F"],
        }
    )
    df.to_csv(external_filename, index=False)
    df.to_csv(internal_filename, index=False)

    return external_filename, internal_filename


@pytest.fixture
def mock_remove_non_printable_chars():
    with mock.patch(
        "data_extraction_utils.remove_non_printable_chars", return_value=lambda x: x
    ):
        yield


@pytest.fixture
def mock_logging():
    with mock.patch("data_extraction_utils.logging") as mock_logging:
        yield mock_logging


def test_download_overwrite_false():
    """Confirm that requests successfully download local copy of file"""
    png_url = "https://raw.githubusercontent.com/cenuno/learning_sql/master/visuals/small_multiples_example.png"
    png_filename = Path(os.path.join("src", "tests", "small_multiples_example.png"))
    download_file(url=png_url, filename=png_filename, overwrite=False)

    assert png_filename.is_file()


def test_download_overwrite_true():
    """Confirm that requests successfully download local copy of file"""
    png_url = "https://raw.githubusercontent.com/cenuno/learning_sql/master/visuals/small_multiples_example.png"
    png_filename = Path(os.path.join("src", "tests", "small_multiples_example.png"))
    download_file(url=png_url, filename=png_filename, overwrite=True)

    assert png_filename.is_file()


def test_download_overwrite_false_existing_file():
    """Confirm that requests successfully download local copy of file"""
    png_url = "https://raw.githubusercontent.com/cenuno/learning_sql/master/visuals/small_multiples_example.png"
    png_filename = Path("README.md")
    download_file(url=png_url, filename=png_filename, overwrite=False)

    assert png_filename.is_file()


def test_download_overwrite_true_existing_file():
    """Confirm that requests successfully download local copy of file"""
    png_url = "https://raw.githubusercontent.com/cenuno/learning_sql/master/visuals/small_multiples_example.png"
    png_filename = Path(os.path.join("src", "tests", "small_multiples_example.png"))
    download_file(url=png_url, filename=png_filename, overwrite=False)

    assert png_filename.is_file()


def test_remove_non_printable_chars():
    test_series = pd.Series(["a", "b", "c", "\x00", "\x07", "\x08", "\x1b"])
    ideal_series = pd.Series(["a", "b", "c", "", "", "", ""])
    output_series = remove_non_printable_chars(series=test_series)
    assert output_series.equals(ideal_series)


def test_process_csv_no_overwrite(setup_files, mock_logging):
    external_filename, internal_filename = setup_files

    # Process the file without overwriting
    internal_filename.touch()
    process_csv(
        client_name="client1",
        client_id=123,
        external_filename=external_filename,
        internal_filename=internal_filename,
        metadata_columns=[
            {
                "position": 0,
                "external_name": "member_id",
                "processed_name": "member_id",
                "data_type": "VARCHAR(5000)",
            },
            {
                "position": 1,
                "external_name": "member_last_name",
                "processed_name": "last_name",
                "data_type": "VARCHAR(5000)",
            },
        ],
        sep=",",
        quoting=1,
        overwrite=False,
    )

    # Check that logging was used correctly and file was not overwritten
    mock_logging.warning.assert_any_call(
        "File already exists and overwrite is false so no need to create file"
    )
    assert internal_filename.exists()


def test_process_csv_with_overwrite(setup_files, mock_logging):
    external_filename, internal_filename = setup_files

    # Ensure internal file is removed to simulate a fresh start
    if internal_filename.exists():
        internal_filename.unlink()

    # Process the file with overwriting
    process_csv(
        client_name="client1",
        client_id=123,
        external_filename=external_filename,
        internal_filename=internal_filename,
        metadata_columns=[
            {
                "position": 0,
                "external_name": "member_id",
                "processed_name": "member_id",
                "data_type": "VARCHAR(5000)",
            },
            {
                "position": 1,
                "external_name": "member_last_name",
                "processed_name": "last_name",
                "data_type": "VARCHAR(5000)",
            },
        ],
        sep=",",
        quoting=1,
        overwrite=True,
    )

    # Check logging and if the file was created
    mock_logging.info.assert_any_call(
        "file does not exist or, if it does, it will be overwritten"
    )
    assert internal_filename.exists()


def test_process_csv_empty_metadata(setup_files, mock_logging):
    external_filename, internal_filename = setup_files

    # Process the file with empty metadata
    process_csv(
        client_name="client1",
        client_id=123,
        external_filename=external_filename,
        internal_filename=internal_filename,
        metadata_columns=[],
        sep=",",
        quoting=1,
        overwrite=True,
    )

    # Check logging and if the file was created with no data
    mock_logging.info.assert_any_call("columns after processing are: []")
    assert internal_filename.exists()


def test_process_csv_invalid_column(setup_files, mock_logging):
    external_filename, internal_filename = setup_files

    # Process the file with invalid metadata
    process_csv(
        client_name="client1",
        client_id=123,
        external_filename=external_filename,
        internal_filename=internal_filename,
        metadata_columns=[
            {
                "position": 0,
                "external_name": "invalid_column",
                "processed_name": "new_name",
                "data_type": "VARCHAR(5000)",
            }
        ],
        sep=",",
        quoting=1,
        overwrite=True,
    )

    # Check that processing logs information about columns
    mock_logging.info.assert_any_call("columns after processing are: []")
    assert internal_filename.exists()


def test_process_csv_logging(setup_files, mock_logging):
    external_filename, internal_filename = setup_files

    # Process the file to ensure all logging points are covered
    process_csv(
        client_name="client1",
        client_id=123,
        external_filename=external_filename,
        internal_filename=internal_filename,
        metadata_columns=[
            {
                "position": 0,
                "external_name": "member_id",
                "processed_name": "member_id",
                "data_type": "VARCHAR(5000)",
            },
            {
                "position": 1,
                "external_name": "member_last_name",
                "processed_name": "last_name",
                "data_type": "VARCHAR(5000)",
            },
        ],
        sep=",",
        quoting=1,
        overwrite=True,
    )

    # Check all logging points
    mock_logging.info.assert_any_call("fetch expected columns")
    mock_logging.info.assert_any_call("ensure all nan values are empty strings")
    mock_logging.info.assert_any_call("for each column, remove non printable chars")
    mock_logging.info.assert_any_call("create hard coded columns with internal_ prefix")
    assert internal_filename.exists()
