#!/usr/bin/python3

"""
Test download_file method
"""

import os
from pathlib import Path

import pandas as pd

from data_extraction_utils import download_file, remove_non_printable_chars


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
    print(test_series)
    print(ideal_series)
    print(output_series)
    assert output_series.equals(ideal_series)
