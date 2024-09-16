#!/usr/bin/python3

"""
Store utility functions and constants in one place
"""

import inspect
import os
from pathlib import Path
import requests
from string import printable
from typing import List, Mapping, Union

import pandas as pd
import pendulum

from custom_logger import setup_function_logger

# NOTE: create custom type
MetadataColumns = List[Mapping[str, Union[str, int, bool]]]

TIMEZONE = "America/Los_Angeles"
CURRENT_SCRIPT_FILENAME = Path(os.path.basename(__file__)).stem


def download_file(url: str, filename: Path, overwrite: bool = False) -> None:
    """Download a file and store it locally

    :param url: str - url that contains a file hosted on the cloud
    :param filename: Path - name of file
    :param overwrite: bool - whether or not to overwrite existing file
    :return: None
    """
    # NOTE: fetch function name
    function_name = inspect.currentframe().f_code.co_name  # type: ignore
    # NOTE: create function logger
    logger = setup_function_logger(
        script_name=CURRENT_SCRIPT_FILENAME, function_name=function_name
    )

    if filename.is_file() and not overwrite:
        logger.warning(
            "File already exists and overwrite is false so no need to download"
        )
    elif not filename.is_file() or (filename.is_file() and overwrite):
        logger.info("file does not exist or, if it does, it will be overwritten")
        logger.info(f"make required dir(s) at {filename.parent}")
        filename.parent.mkdir(parents=True, exist_ok=True)

        logger.info("downloading file from internet")
        content = requests.get(url).content

        logger.info(f"write a copy of binary data to the {filename} file")
        with open(filename, "wb") as file:
            file.write(content)


def remove_non_printable_chars(series: pd.Series) -> pd.Series:
    """For a column in a df, remove non printable chars

    :param series: pd.Series - the relevant column in a df
    :return: series - a series without non printable characters
    """
    # NOTE: fetch function name
    function_name = inspect.currentframe().f_code.co_name  # type: ignore
    # NOTE: create function logger
    logger = setup_function_logger(
        script_name=CURRENT_SCRIPT_FILENAME, function_name=function_name
    )

    logger.info(f"removing non printable chars from the series: {series.name}")
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
    metadata_columns: MetadataColumns,
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
    :param metadata_columns: Metadata Columns - an array that contains one dictionary per given column
    :param sep: str - the delimiter used to separate columns within a row
    :param quoting: int - the quote option of preference
    :param overwrite: bool - whether or not to overwrite existing file

    :return: None
    """
    # NOTE: fetch function name
    function_name = inspect.currentframe().f_code.co_name  # type: ignore
    # NOTE: create function logger
    logger = setup_function_logger(
        script_name=CURRENT_SCRIPT_FILENAME, function_name=function_name
    )

    if internal_filename.is_file() and not overwrite:
        logger.warning(
            "File already exists and overwrite is false so no need to create file"
        )
    elif not internal_filename.is_file() or (internal_filename.is_file() and overwrite):
        logger.info("file does not exist or, if it does, it will be overwritten")
        logger.info(f"make required dir(s) at {internal_filename.parent}")
        internal_filename.parent.mkdir(parents=True, exist_ok=True)

        logger.info(f"read in data from {external_filename}")
        # NOTE: hard code to read from first sheet and ensure data types are all strings
        df_raw = pd.read_csv(
            filepath_or_buffer=external_filename,
            dtype=str,
        )
        logger.info(f"columns as is are: {list(df_raw.columns)}")

        logger.info("create empty data frame")
        df_processed = pd.DataFrame()

        logger.info("create internal column mapping")
        # NOTE: create constant time
        NOW = pendulum.now(tz=TIMEZONE)
        INTERNAL_COLUMNS_NOT_FOUND_IN_FILE = {
            "client_name": client_name,
            "client_id": client_id,
            "external_filename": str(external_filename),
            "internal_filename": str(internal_filename),
            "created_on": NOW,
            "modified_on": NOW,
        }

        logger.info("fetch expected columns")
        for ind, expected_column_data in enumerate(metadata_columns):
            # NOTE: unpack keys
            position = expected_column_data["position"]
            external_name = expected_column_data["external_name"]
            processed_name = expected_column_data["processed_name"]
            found_in_file = expected_column_data["found_in_file"]
            # NOTE: for columns found in the file
            if found_in_file:
                logger.info(f"looking for {external_name} from dataset")
                # NOTE: fetch all columns found in the file
                for given_column in df_raw.columns:
                    # NOTE: ensure the expected name and position align
                    if external_name == given_column and ind == position:
                        # NOTE: create a new column
                        df_processed[processed_name] = df_raw[given_column]
            else:
                # NOTE: for columns not found in file, they're internal columns
                for (
                    internal_column,
                    value,
                ) in INTERNAL_COLUMNS_NOT_FOUND_IN_FILE.items():
                    # NOTE: check if this internal column matches the one currently being processed
                    if internal_column == processed_name:
                        logger.info(f"processing internal columns of: {processed_name}")
                        df_processed[processed_name] = value

        logger.info(f"columns after processing are: {list(df_processed.columns)}")

        logger.info("ensure all nan values are empty strings")
        df_processed = df_processed.fillna("")

        logger.info("for each object column, remove non printable chars")
        for col, dtype in zip(df_processed.columns, df_processed.dtypes):
            if pd.api.types.is_object_dtype(dtype):
                df_processed[col] = remove_non_printable_chars(df_processed[col])

        logger.info(
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
