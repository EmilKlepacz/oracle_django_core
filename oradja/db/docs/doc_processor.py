import logging
import time
from typing import Optional

from oradja.file_manager.file_manager import FileManager
from oradja.file_manager.file_type import FileType
from oradja.models import UmvDocument

logger = logging.getLogger("django")


def _download_file_name(doc: dict) -> str:
    return "_".join([str(doc["umvdcm"]), doc["file_name"].replace("/", "")])


class DocProcessor:
    def __init__(self, file_manager: Optional[FileManager]):
        self._file_manager = file_manager
        self._file_types = None

    @property
    def file_types(self):
        if self._file_types is None:
            self._file_types = FileType.all()
        return self._file_types

    @file_types.setter
    def file_types(self, value):
        if not isinstance(value, list):
            raise ValueError("value must be a list.")
        if not all(isinstance(ft, FileType) for ft in value):
            raise ValueError("All items in list must be instances of FileType.")
        self._file_types = value

    def download(self, **kwargs):
        self._file_manager.new_dir()
        docs = UmvDocument.query_docs(fetch_file_blob=True,
                                      **kwargs)

        start_time = time.time()
        logger.info(f"Start downloading {len(docs)} files...")

        for doc in docs:
            download_file_path = self._file_manager.last_created_dir_path / _download_file_name(doc)
            try:
                with open(download_file_path, "xb") as file:
                    file.write(doc["file_data"])
            except FileExistsError:
                logger.info(
                    f"'{download_file_path}' was skipped as already exist")

        elapsed_time = time.time() - start_time
        logger.info(f"Finished downloading {len(docs)} files in {elapsed_time:.2f} seconds.")
