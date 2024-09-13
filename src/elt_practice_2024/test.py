from client_data_manager import ClientDataManager
from pathlib import Path

CLIENT_DATA_SOURCES_PATH = Path("client_data_sources.json")
cdm = ClientDataManager(client_name="acme", data_path=CLIENT_DATA_SOURCES_PATH)
cdm.download_and_process_files()
