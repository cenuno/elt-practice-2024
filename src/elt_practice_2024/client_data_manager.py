#!/usr/bin/python3

"""
Create a custom class to handle client data
"""

import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Tuple

from data_extraction_utils import download_file, process_csv


class ClientDataManager:
    def __init__(self, client_name: str, data_path: str):
        """
        Initialize the ClientDataManager with a client name and path to the JSON data.

        :param client_name: str - Name of the client
        :param data_path: str - Path to JSON-like data containing client information
        """
        with open(data_path, mode="r", encoding="utf-8") as f:
            self.client_data_sources = json.load(f)
        self.client_name = client_name
        self.client_data = self._get_client_data()
        self.client_id = self.client_data["client_id"]

    def _get_client_data(self) -> dict:
        """
        Private method to get data for the specified client.

        :return: dict - Data specific to the client, if exists
        """
        for client in self.client_data_sources:
            if client["client_name"] == self.client_name:
                return client
        raise ValueError(f"No data available for client: {self.client_name}")

    def get_file_types(self) -> List[str]:
        """
        Retrieve the available file types for the client.

        :return: list - List of available file types
        """
        return list(self.client_data["file_types"].keys())

    def get_files_by_type(self, file_type: str) -> List[Dict[str, str]]:
        """
        Retrieve the list of files for a given file type.

        :param file_type: str - The type of files to retrieve (e.g., 'membership')
        :return: list - List of files with their metadata
        """
        file_data = self.client_data["file_types"].get(file_type)
        if not file_data:
            raise ValueError(f"No files found for the type: {file_type}")
        return file_data["files"]

    def get_metadata_by_file_type(self, file_type: str) -> Dict[str, str]:
        """
        Retrieve metadata for a given file type.

        :param file_type: str - The type of files to retrieve metadata for (e.g., 'membership')
        :return: dict - Metadata related to the file type
        """
        file_data = self.client_data["file_types"].get(file_type)
        if not file_data:
            raise ValueError(f"No metadata found for the type: {file_type}")
        return file_data["metadata"]

    def download_and_process_files(
        self,
        file_types: List[str] = [],
        input_dir: str = ".",
        output_dir: str = ".",
        sep: str = "|",
        quoting: int = 3,
        overwrite_download: bool = False,
        overwrite_process: bool = False,
    ) -> None:
        """Loop through the files across file types, download and process them

        :param file_types: List[str]: a list of file types. Assumed all if None.
        :param input_dir: str - location of the downloaded external files
        :param output_dir: str - location of the processed files
        :param sep: str - the delimiter used to separate columns within a row
        :param quoting: int - the quote option of preference
        :param overwrite_download: bool - whether or not to overwrite the downloaded file
        :param overwrite_process: bool - whether or not to overwrite the processed file

        :return: None
        """
        # Step 1: Get the list of relevant file types
        relevant_file_types = self._get_relevant_file_types(file_types)

        # Step 2: Process each relevant file type
        for file_type in relevant_file_types:
            files, metadata_columns = self._get_files_and_metadata(file_type)
            for file in files:
                self._download_and_process_file(
                    file=file,
                    metadata_columns=metadata_columns,
                    input_dir=input_dir,
                    output_dir=output_dir,
                    sep=sep,
                    quoting=quoting,
                    overwrite_download=overwrite_download,
                    overwrite_process=overwrite_process,
                    file_type=file_type,
                )

    def _get_relevant_file_types(self, file_types: List[str]) -> List[str]:
        """Retrieve relevant file types for processing.

        :param file_types: List[str] - The file types to process, or all known types if empty
        :return: List[str] - List of relevant file types
        """
        logging.info("retrieving relevant files based on user input")
        known_file_types = self.get_file_types()

        # If no specific file types are provided, process all known file types
        if not file_types:
            return known_file_types

        # Check if provided file types are valid
        unknown_file_types = [
            file_type for file_type in file_types if file_type not in known_file_types
        ]
        if unknown_file_types:
            raise ValueError(f"Unknown file type given: {unknown_file_types}")

        return file_types

    def _get_files_and_metadata(
        self, file_type: str
    ) -> Tuple[List[Dict[str, str]], List[str]]:
        """Retrieve the list of files and associated metadata columns for the given file type.

        :param file_type: str - The type of files to retrieve
        :return: Tuple[List[Dict[str, str]], List[str]] - List of files and metadata columns
        """
        logging.info(
            "retrieving the list of files and associated metadata columns for the given file type"
        )
        files = self.get_files_by_type(file_type)
        metadata = self.get_metadata_by_file_type(file_type)
        return files, metadata["columns"]

    def _download_and_process_file(
        self,
        file: Dict[str, str],
        metadata_columns: List[str],
        input_dir: str,
        output_dir: str,
        sep: str,
        quoting: int,
        overwrite_download: bool,
        overwrite_process: bool,
        file_type: str,
    ) -> None:
        """Download and process a single file based on metadata and client settings.

        :param file: Dict[str, str] - A dictionary with file information (e.g., URL, filenames)
        :param metadata_columns: List[str] - The metadata columns required for processing the file
        :param input_dir: str - Location of the downloaded external files
        :param output_dir: str - Location of the processed files
        :param sep: str - Delimiter used in the file
        :param quoting: int - Quote option to use during file processing
        :param overwrite_download: bool - Whether to overwrite an already downloaded file
        :param overwrite_process: bool - Whether to overwrite an already processed file
        :param file_type: str - Type of file being processed (e.g., 'membership')

        :return: None
        """
        external_filename = Path(os.path.join(input_dir, file["external_filename"]))
        external_url = file["external_url"]
        internal_filename = Path(os.path.join(output_dir, file["internal_filename"]))

        logging.info(
            f"Inspecting if it is necessary for client {self.client_name}, file type {file_type}, "
            f"downloading URL {external_url} locally to {external_filename}"
        )

        # Download the file
        download_file(
            url=external_url,
            filename=external_filename,
            overwrite=overwrite_download,
        )

        logging.info("Inspect if we need to process the external file")

        # Process the downloaded file
        process_csv(
            client_name=self.client_name,
            client_id=self.client_id,
            external_filename=external_filename,
            internal_filename=internal_filename,
            metadata_columns=metadata_columns,
            sep=sep,
            quoting=quoting,
            overwrite=overwrite_process,
        )
