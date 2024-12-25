import logging
import time

from oradja.file_manager.file_manager import FileManager
from oradja.models import UmvDocument

logger = logging.getLogger("django")


def _download_file_name(doc: dict) -> str:
    return "_".join([str(doc["umvdcm"]), doc["file_name"].replace("/", "")])


class DocProcessor:
    def __init__(self, file_manager: FileManager):
        self.file_manager = file_manager

    def download(self, **kwargs):
        self.file_manager.new_dir()
        docs = UmvDocument.query_docs(fetch_file_blob=True, **kwargs)

        start_time = time.time()
        logger.info(f"Start downloading {len(docs)} files...")

        for doc in docs:
            download_file_path = self.file_manager.last_created_dir_path / _download_file_name(doc)
            try:
                with open(download_file_path, "xb") as file:
                    file.write(doc["file_data"])
            except FileExistsError:
                logger.info(
                    f"'{download_file_path}' was skipped as already exist")

        elapsed_time = time.time() - start_time
        logger.info(f"Finished downloading {len(docs)} files in {elapsed_time:.2f} seconds.")
