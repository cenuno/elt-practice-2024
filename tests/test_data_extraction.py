#!/usr/bin/python3

"""
Test download_file method
"""


def test_data_extraction():
    import os
    from pathlib import Path

    data_dir = Path(
        os.path.join(
            "src", "elt_practice_2024", "data", "input", "Interview Sample Files"
        )
    )
    assert sum(1 for _ in data_dir.iterdir()) == 6
