#!/usr/bin/python3

"""
Test download_file method
"""


def test_data_file_count():
    import os
    from pathlib import Path

    from data_extraction import excel_filenames

    data_dir = Path(
        os.path.join(
            "src", "elt_practice_2024", "data", "input", "Interview Sample Files"
        )
    )
    
    assert sum(1 for _ in data_dir.iterdir()) == len(excel_filenames)
