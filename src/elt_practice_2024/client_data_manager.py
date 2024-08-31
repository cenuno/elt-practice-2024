#!/usr/bin/python3

"""
Create a custom class to handle client data
"""

import json
from typing import List


class ClientDataManager:
    def __init__(self, client_name: str, data_path: str):
        """
        Initialize the ClientDataManager with client name and data.

        :param client_name: str - Name of the client
        :param data_path: str - relative path to JSON-like data containing client information
        """
        # NOTE: open json and load as dict
        with open(data_path, mode="r", encoding="utf-8") as f:
            client_data_sources = json.load(f)
        self.client_name = client_name
        self.data = client_data_sources
        self.client_data = self._get_client_data()

    def _get_client_data(self):
        """
        Private method to get data for the specified client.

        :return: dict - Data specific to the client, if exists
        """
        client_data = self.data.get(self.client_name)
        if not client_data:
            raise ValueError(f"No data available for client: {self.client_name}")
        return client_data

    def get_file_types(self) -> List[str]:
        """
        Retrieve the types of files available for the client.

        :return: list - List of available file types
        """
        return list(self.client_data.keys())

    def get_file_names(self, file_type: str) -> List[str]:
        """
        Retrieve the file names for the specified file type.

        :param file_type: str - Type of files to retrieve (e.g., 'membership_files')
        :return: list - List of file names for the specified type
        """
        files = self.client_data.get(file_type)
        if not files:
            raise ValueError(f"No files found for the type: {file_type}")
        return list(files.keys())

    def get_file_data(self, file_type: str, file_name: str) -> dict[str, str]:
        """
        Retrieve data about a specific file.

        :param file_type: str - Type of files (e.g., 'membership_files')
        :param file_name: str - Specific file name to retrieve data
        :return: dict - Data about the file (URL, Excel filename, CSV filename)
        """
        files = self.client_data.get(file_type)
        if not files:
            raise ValueError(f"No files found for the type: {file_type}")

        file_data = files.get(file_name)
        if not file_data:
            raise ValueError(f"No data found for the file: {file_name}")

        return file_data

    def get_all_filenames(self) -> tuple[List[str], List[str]]:
        """
        Retrieves all Excel and CSV filenames across all clients and all file types.

        :return: tuple - list of excel filenames followed by csv filenames
        """
        excel_files = []
        csv_files = []

        # Iterate over all clients in the data
        for client_data in self.data.values():
            # Iterate over all file types within the client (e.g., membership_files, claim_files)
            for files in client_data.values():
                # Iterate over each file's data to collect Excel and CSV filenames
                for file_info in files.values():
                    if "excel_filename" in file_info:
                        excel_files.append(file_info["excel_filename"])
                    if "csv_filename" in file_info:
                        csv_files.append(file_info["csv_filename"])

        return excel_files, csv_files
