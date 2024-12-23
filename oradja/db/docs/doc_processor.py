import logging
import time

from oradja.file_manager.file_manager import FileManager
from oradja.models import UmvDocument

logger = logging.getLogger("django")


class DocProcessor:
    def __init__(self, file_manager: FileManager):
        self.file_manager = file_manager

    def download(self, **kwargs):
        self.file_manager.new_dir()
        docs = UmvDocument.query_docs(fetch_file_blob=True, **kwargs)

        start_time = time.time()
        logger.info(f"Start downloading {len(docs)} files...")

        for doc in docs:
            file_name_unique = "_".join([str(doc["umvdcm"]), doc["file_name"].replace("/", "")])

            try:
                with open(self.file_manager.last_created_dir / file_name_unique, "xb") as file:
                    file.write(doc["file_data"])
            except FileExistsError:
                logger.info(f"'{self.file_manager.last_created_dir / file_name_unique / file_name_unique}' was skipped as already exist")

        elapsed_time = time.time() - start_time
        logger.info(f"Finished downloading {len(docs)} files in {elapsed_time:.2f} seconds.")
