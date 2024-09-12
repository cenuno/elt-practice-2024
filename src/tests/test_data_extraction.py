import json
import os
import csv
from pathlib import Path

from client_data_manager import ClientDataManager
from data_extraction_utils import process_csv

# Define the path to the test data and create mock data
CLIENT_DATA_SOURCES_PATH = Path('test_client_data_sources.json')
TEST_DATA = [
        {
            "client_name": "acme",
            "client_id": 1,
            "file_types": {
                "membership": {
                    "files": [
                        {
                            "external_filename": "external_file.xlsx",
                            "external_url": "http://example.com/external_file.xlsx",
                            "internal_filename": "internal_file.csv"
                        }
                    ],
                    "metadata": {
                        "columns": [
                            {"position": 0, "external_name": "name", "processed_name": "Name"},
                            {"position": 1, "external_name": "age", "processed_name": "Age"}
                        ],
                        "schema_name": "public",
                        "table_name": "members"
                    }
                }
            }
        },
        {
            "client_name": "hooli"
        }
]

# Write the test data to a JSON file
with open(CLIENT_DATA_SOURCES_PATH, 'w', encoding='utf-8') as f:
    json.dump(TEST_DATA, f, indent=4)

# Test ClientDataManager
def test_client_data_manager():
    client_manager = ClientDataManager(client_name="acme", data_path=CLIENT_DATA_SOURCES_PATH)

    # Test get_file_types
    assert client_manager.get_file_types() == ["membership"]

    # Test get_files_by_type
    files = client_manager.get_files_by_type("membership")
    assert len(files) == 1
    assert files[0]["external_filename"] == "external_file.xlsx"

    # Test get_metadata_by_file_type
    metadata = client_manager.get_metadata_by_file_type("membership")
    assert metadata["schema_name"] == "public"
    assert metadata["table_name"] == "members"

    # Test get_all_filenames
    filenames = client_manager.get_all_filenames()
    assert "membership" in filenames
    assert len(filenames["membership"]["external_filenames"]) == 1
    assert filenames["membership"]["external_filenames"][0].name == "external_file.xlsx"

# Test process_csv
def test_process_csv():
    # Define dummy data and paths
    external_filename = Path('test_external_file.csv')
    internal_filename = Path('test_internal_file.csv')
    metadata_columns = [
        {"position": 0, "external_name": "name", "processed_name": "Name"},
        {"position": 1, "external_name": "age", "processed_name": "Age"}
    ]

    # Create a dummy CSV file
    with open(external_filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["name", "age"])
        writer.writerow(["Alice", "30"])
        writer.writerow(["Bob", "25"])

    # Call the function
    process_csv(
        client_name="acme",
        client_id=1,
        external_filename=external_filename,
        internal_filename=internal_filename,
        metadata_columns=metadata_columns,
        sep=',',
        quoting=csv.QUOTE_MINIMAL
    )

    # Check if the internal file was created
    assert internal_filename.is_file()

    # Clean up
    os.remove(external_filename)
    os.remove(internal_filename)

# Clean up the test data file
def teardown_module():
    if os.path.isfile(CLIENT_DATA_SOURCES_PATH):
        os.remove(CLIENT_DATA_SOURCES_PATH)
