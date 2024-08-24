#!/usr/bin/python3

"""
Test download_file method
"""


def test_download_overwrite_false():
    """Confirm that requests successfully download local copy of file"""
    import os
    from pathlib import Path
    
    from elt_practice_2024.utils import download_file

    png_url = "https://raw.githubusercontent.com/cenuno/learning_sql/master/visuals/small_multiples_example.png"
    png_filename = Path(os.path.join("tests", "small_multiples_example.png"))
    download_file(url=png_url, filename=png_filename, overwrite=False)

    assert png_filename.is_file()


def test_download_overwrite_true():
    """Confirm that requests successfully download local copy of file"""
    import os
    from pathlib import Path

    from elt_practice_2024.utils import download_file

    png_url = "https://raw.githubusercontent.com/cenuno/learning_sql/master/visuals/small_multiples_example.png"
    png_filename = Path(os.path.join("tests", "small_multiples_example.png"))
    download_file(url=png_url, filename=png_filename, overwrite=True)

    assert png_filename.is_file()

def test_download_overwrite_false_existing_file():
    """Confirm that requests successfully download local copy of file"""
    import os
    from pathlib import Path

    from elt_practice_2024.utils import download_file

    png_url = "https://raw.githubusercontent.com/cenuno/learning_sql/master/visuals/small_multiples_example.png"
    png_filename = Path("README.md")
    download_file(url=png_url, filename=png_filename, overwrite=False)

    assert png_filename.is_file()

def test_download_overwrite_true_existing_file():
    """Confirm that requests successfully download local copy of file"""
    import os
    from pathlib import Path

    from elt_practice_2024.utils import download_file

    png_url = "https://raw.githubusercontent.com/cenuno/learning_sql/master/visuals/small_multiples_example.png"
    png_filename = Path(os.path.join("tests", "small_multiples_example.png"))
    download_file(url=png_url, filename=png_filename, overwrite=False)

    assert png_filename.is_file()
