import os
import json
from typing import Any, Dict, List
from utils.functions import mkdirs
from utils.settings import lazy_settings


class MacroFileORM:
    def __init__(self, table: str):
        """
        Initialize the ORM with a specific table (entity name).
        """
        self.table = table
        self.file = self._get_file_path()
        self._ensure_file_exists()

    def _get_file_path(self) -> str:
        """
        Returns the file path for storing data based on the table name.
        """
        return os.path.join(
            lazy_settings.DATA_STORAGE_DIR,
            f"{self.table}.{lazy_settings.DATA_STORAGE_FORMAT}",
        )

    def _ensure_file_exists(self):
        """
        Ensure the data file exists, creating it if does'nt exists.
        """
        if not os.path.exists(self.file):
            mkdirs(self.file, is_file=True)
            with open(self.file, "w") as file:
                json.dump([], file)

    def _read_data(self) -> List[Dict[str, Any]]:
        """
        Read all data from the file.
        """
        try:
            with open(self.file, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _write_data(self, data: List[Dict[str, Any]]):
        """
        Writes all given data to the file.
        """
        with open(self.file, "w") as file:
            json.dump(data, file, indent=4)

    def create(self, record: Dict[str, Any]):
        """
        Adds a new instance of the entity to the data file.
        """
        data = self._read_data()
        data.append(record)
        self._write_data(data)

    def read(self, **filters) -> List[Dict[str, Any]]:
        """
        Retrieve records matching the given filters.
        """
        records = self._read_data()
        if not filters:
            return records
        return [
            record
            for record in records
            if all(record.get(k) == v for k, v in filters.items())
        ]

    def update(self, filters: Dict[str, Any], **updates):
        """
        Update instances matching the given filters with new data.
        """
        records = self._read_data()
        updated = False

        for record in records:
            if all(record.get(k) == v for k, v in filters.items()):
                record.update(updates)
                updated = True

        if updated:
            self._write_data(records)

    def delete(self, **filters):
        """
        Delete instances matching the given filters.
        I'm so tired of writing docstrings. #1
        """
        records = self._read_data()
        filtered_records = [
            record
            for record in records
            if not all(record.get(k) == v for k, v in filters.items())
        ]

        if len(filtered_records) != len(records):  # Only write if something was deleted
            self._write_data(filtered_records)

    def get_next_id(self) -> int:
        """
        Generate the next available ID for the table.
        """
        records = self._read_data()
        lookup = lazy_settings.PRIMARY_KEY_LOOKUP
        return max((record.get(lookup, 0) for record in records), default=0) + 1
