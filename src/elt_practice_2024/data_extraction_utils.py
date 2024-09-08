#!/usr/bin/python3

"""
Store utility functions and constants in one place
"""

import logging
from pathlib import Path
import requests
from string import printable
from typing import Dict, List

import pandas as pd
import pendulum

TIMEZONE = "America/Los_Angeles"


# NOTE: create custom functions
def download_file(url: str, filename: Path, overwrite: bool = False) -> None:
    """Download a file and store it locally

    :param url: str - url that contains a file hosted on the cloud
    :param filename: Path - name of file
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


def process_csv(
    client_name: str,
    client_id: int,
    external_filename: Path,
    internal_filename: Path,
    metadata_columns: List[Dict],
    sep: str,
    quoting: int,
    overwrite: bool = False,
) -> None:
    """Read in raw file, process it, and generate csv file

    NOTE:
        Ideally we do as little processing as possible here but
        it's inevitable when working with partner data.
    :param client_name: str - name of client
    :param client_id: int - ID of client
    :param external_filename: Path - file path of external file
    :param internal_filename: Path - file path of internal file
    :param metadata_columns: List[Dict] - an array that contains one dictionary per given column
    :param sep: str - the delimiter used to separate columns within a row
    :param quoting: int - the quote option of preference
    :param overwrite: bool - whether or not to overwrite existing file

    :return: None
    """
    if internal_filename.is_file() and not overwrite:
        logging.warning(
            "File already exists and overwrite is false so no need to create file"
        )
    elif not internal_filename.is_file() or (internal_filename.is_file() and overwrite):
        logging.info("file does not exist or, if it does, it will be overwritten")
        logging.info(f"make required dir(s) at {internal_filename.parent}")
        internal_filename.parent.mkdir(parents=True, exist_ok=True)

        logging.info(f"read in data from {external_filename}")
        # NOTE: hard code to read from first sheet and ensure data types are all strings
        df_raw = pd.read_csv(
            filepath_or_buffer=external_filename,
            dtype=str,
        )
        logging.info(f"columns as is are: {list(df_raw.columns)}")

        # NOTE: create empty data frame
        df_processed = pd.DataFrame()

        logging.info("fetch expected columns")
        for ind, expected_column_data in enumerate(metadata_columns):
            # NOTE: unpack keys
            position = expected_column_data["position"]
            external_name = expected_column_data["external_name"]
            processed_name = expected_column_data["processed_name"]
            logging.info(f"looking for {external_name} from dataset")
            for given_column in df_raw.columns:
                if external_name == given_column and ind == position:
                    df_processed[processed_name] = df_raw[given_column]

        logging.info(f"columns after processing are: {list(df_processed.columns)}")

        logging.info("ensure all nan values are empty strings")
        df_processed = df_processed.fillna("")

        logging.info("for each column, remove non printable chars")
        for col in df_processed.columns:
            df_processed[col] = remove_non_printable_chars(df_processed[col])

        logging.info("create hard coded columns with internal_ prefix")
        df_processed["client_name"] = client_name
        df_processed["client_id"] = client_id
        df_processed["external_filename"] = external_filename
        df_processed["internal_filename"] = internal_filename
        # NOTE: create constant time
        NOW = pendulum.now(tz=TIMEZONE)
        df_processed["created_on"] = NOW
        df_processed["modified_on"] = NOW
        logging.info(f"final columns are: {df_processed.columns}")

        logging.info(
            f"generate {internal_filename} where "
            f"each cell is separated via a {sep} and {quoting} quote option"
        )
        df_processed.to_csv(
            path_or_buf=internal_filename,
            index=False,
            quoting=quoting,
            sep=sep,
        )

        return None
