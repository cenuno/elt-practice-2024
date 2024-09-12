#!/usr/bin/python3

"""
Create a custom class to handle client data
"""

import json
from pathlib import Path
from typing import List, Dict


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

    def get_all_filenames(self) -> Dict[str, Dict[str, List[Path]]]:
        """
        Retrieves all filenames for the client and file type

        :return: dict - each key that contains a list of file paths
        """
        filenames = dict()  # type: Dict[str, Dict[str, List[Path]]]
        for file_type in self.get_file_types():
            filenames[file_type] = dict()
            files = self.get_files_by_type(file_type)
            print(files)
            filenames[file_type]["internal_filenames"] = []
            filenames[file_type]["external_filenames"] = []
            for file in files:
                filenames[file_type]["internal_filenames"].append(
                    Path(file["internal_filename"])
                )
                filenames[file_type]["external_filenames"].append(
                    Path(file["external_filename"])
                )

        return filenames
