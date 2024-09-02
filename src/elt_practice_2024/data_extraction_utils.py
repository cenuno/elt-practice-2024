#!/usr/bin/python3

"""
Store utility functions and constants in one place
"""

import logging
import pathlib
import requests
from string import printable

import pandas as pd
import pendulum

TIMEZONE = "America/Los_Angeles"


# NOTE: create custom functions
def download_file(url: str, filename: pathlib.Path, overwrite: bool = False) -> None:
    """Download a file and store it locally

    :param url: str - url that contains a file hosted on the cloud
    :param filename: pathlib.Path - name of file
    :param overwrite: bool - whether or not to overwrite existing file
    :return: None
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


def remove_non_printable_chars(series: pd.Series) -> pd.Series:
    """For a column in a df, remove non printable chars

    :param series: pd.Series - the relevant column in a df
    :return: series - a series without non printable characters
    """
    # NOTE: store printable chars in a set
    printable_chars = set(printable)

    # NOTE: replace non printable chars with empty string
    #       else, leave char as is
    output_col = series.apply(
        lambda row: "".join(
            ["" if char not in printable_chars else char for char in row]
        )
    )
    # NOTE: cast to a series
    output_series = pd.Series(output_col)

    return output_series


def read_in_excel_and_generate_csv(file_data: dict) -> None:
    """Read in the first sheet within an excel file and produce a csv file

    NOTE:
        Ideally we do as little processing as possible here but
        it's inevitable when working with partner data.
    :param file_data: dic - file data dictionary from ClientDataManager class
    :return: None
    """
    logging.info(f"read in the first sheet from {excel_path}")
    # NOTE: hard code to read from first sheet and ensure data types are all strings
    df_excel_first_sheet = pd.read_excel(
        io=excel_path,
        sheet_name=0,
        dtype=str,
        engine="openpyxl",
    )

    # NOTE: add in an index column for row indentification
    df_excel_first_sheet = df_excel_first_sheet.rename_axis("id").reset_index()

    logging.info("ensure all nan values are empty strings")
    df_excel_first_sheet = df_excel_first_sheet.fillna("")

    logging.info("determine which columns need non printable characters removed")
    for col in df_excel_first_sheet.columns:
        logging.info("remove non printable chars")
        df_excel_first_sheet[col] = _remove_non_printable_chars(
            df_excel_first_sheet[col]
        )

    logging.info("create hard coded columns with internal_ prefix")
    df_excel_first_sheet["internal_client_name"]
    df_excel_first_sheet["internal_file_type"]
    df_excel_first_sheet["internal_file_name"]
    df_excel_first_sheet["internal_created_on"] = pendulum.now(tz=TIMEZONE)

    logging.info(
        f"export as csv with an index to {csv_path} and "
        "each cell is separated via a vertical pipe delimiter"
    )
    df_excel_first_sheet.to_csv(
        path_or_buf=csv_path, index=False, quoting=csv.QUOTE_NONE, sep="|"
    )

    return None
