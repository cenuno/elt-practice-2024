#!/usr/bin/python3

"""
Create a custom class to handle client data.
"""

import json
from pathlib import Path
from typing import List, Dict


class ClientDataManager:
    def __init__(self, client_name: str, data_path: str):
        """
        Initialize the ClientDataManager with client name and data.

        :param client_name: str - Name of the client
        :param data_path: str - Relative path to JSON-like data containing client information

        Example usage:
        --------------
        >>> manager = ClientDataManager("acme", "data/clients.json")
        """
        # Load JSON data and set up client-specific data
        with open(data_path, mode="r", encoding="utf-8") as f:
            client_data_sources = json.load(f)

        self.client_data = self._get_client_data(client_data_sources)
        self.client_name = client_name
        self.client_id = self._get_client_data(client_data_sources).get("client_id")

    def _get_client_data(self, client_data_sources: List[Dict]) -> Dict:
        """
        Private method to get data for the specified client.

        :param client_data_sources: List[Dict] - The data loaded from the JSON file.
        :return: dict - Data specific to the client, if exists

        Example usage:
        --------------
        >>> manager = ClientDataManager("acme", "data/clients.json")
        >>> client_data = manager._get_client_data([{"client_name": "acme", ...}])
        """
        for client in client_data_sources:
            if client["client_name"] == self.client_name:
                return client
        raise ValueError(f"No data available for client: {self.client_name}")

    def get_file_types(self) -> List[str]:
        """
        Retrieve the types of files available for the client.

        :return: list - List of available file types

        Example usage:
        --------------
        >>> manager = ClientDataManager("acme", "data/clients.json")
        >>> file_types = manager.get_file_types()
        """
        return list(self.client_data["file_types"].keys())

    def get_file_names(self, file_type: str) -> List[str]:
        """
        Retrieve the file names for the specified file type.

        :param file_type: str - Type of files to retrieve (e.g., 'membership', 'claim')
        :return: list - List of file names for the specified type

        Example usage:
        --------------
        >>> manager = ClientDataManager("acme", "data/clients.json")
        >>> file_names = manager.get_file_names("membership")
        """
        if file_type not in self.client_data["file_types"]:
            raise ValueError(f"No file type found: {file_type}")
        return [
            f["external_filename"]
            for f in self.client_data["file_types"][file_type]["files"]
        ]

    def get_file_data(self, file_type: str, external_filename: str) -> Dict[str, str]:
        """
        Retrieve data about a specific file.

        :param file_type: str - Type of files (e.g., 'membership', 'claim')
        :param external_filename: str - Specific external filename to retrieve data
        :return: dict - Data about the file (URL, external filename, internal filename)

        Example usage:
        --------------
        >>> manager = ClientDataManager("acme", "data/clients.json")
        >>> file_data = manager.get_file_data("membership", "data/input/acme_patient_membership_202307.xlsx")
        """
        files = self.client_data["file_types"].get(file_type, {}).get("files", [])
        for file_info in files:
            if file_info["external_filename"] == external_filename:
                return file_info
        raise ValueError(f"No data found for the file: {external_filename}")

    def get_metadata(self, file_type: str) -> Dict:
        """
        Retrieve metadata for a specific file type.

        :param file_type: str - Type of files (e.g., 'membership', 'claim')
        :return: dict - Metadata about the file type (columns, schema, table name)

        Example usage:
        --------------
        >>> manager = ClientDataManager("acme", "data/clients.json")
        >>> metadata = manager.get_metadata("membership")
        """
        return self.client_data["file_types"].get(file_type, {}).get("metadata", {})

    def get_all_filenames(self) -> Dict[str, List[Path]]:
        """
        Retrieves all external and internal filenames across all file types for the client.

        :return: dict - Dictionary containing lists of external and internal filenames

        Example usage:
        --------------
        >>> manager = ClientDataManager("acme", "data/clients.json")
        >>> filenames = manager.get_all_filenames()
        """
        external_files = []
        internal_files = []
        for file_type in self.get_file_types():
            for file_info in self.client_data["file_types"][file_type]["files"]:
                external_files.append(Path(file_info["external_filename"]))
                internal_files.append(Path(file_info["internal_filename"]))
        return {
            "external_filenames": external_files,
            "internal_filenames": internal_files,
        }
