#!/usr/bin/python3

"""
Test the extraction of data from cloud and that it is stored locally
"""


def test_download():
    """Confirm that requests successfully download local copy of file"""
    import os
    from pathlib import Path

    from elt_practice_2024.data_extraction import download_file

    png_url = "https://raw.githubusercontent.com/cenuno/learning_sql/master/visuals/small_multiples_example.png"
    png_filename = Path(os.path.join("tests", "small_multiples_example.png"))

    download_file(url=png_url, filename=png_filename)

    assert png_filename.is_file()
    # NOTE: remove file after test
    png_filename.unlink()
