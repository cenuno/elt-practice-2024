#!/usr/bin/python3

"""
Store utility functions and constants in one place
"""

import logging
import pathlib
import requests


# NOTE: create custom functions
def download_file(url: str, filename: pathlib.Path, overwrite: bool = False) -> None:
    """Download a file and store it locally

    Args:
        url (str): url that contains a file hosted on the cloud
        filename (pathlib.Path): name of file
        overwrite (bool): whether or not to overwrite existing file
    Returns:
        None
    """

    if filename.is_file() and not overwrite:
        logging.warning(
            "File already exists and overwrite is false so no need to download"
        )
    elif not filename.is_file() or (filename.is_file() and overwrite):
        logging.info("file does not exist or, if it does, it will be overwritten")
        logging.info(f"make required dir(s) at {filename.parent}")
        filename.parent.mkdir(parents=True, exist_ok=True)

        logging.info("downloading file from internet")
        content = requests.get(url).content

        logging.info(f"write a copy of binary data to the {filename} file")
        with open(filename, "wb") as file:
            file.write(content)
