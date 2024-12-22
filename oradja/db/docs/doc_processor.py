import logging
import sys

from oradja.file_manager.file_manager import FileManager
from oradja.models import UmvDocument

logger = logging.getLogger("django")


class DocProcessor:
    def __init__(self, file_manager: FileManager):
        self.file_manager = file_manager

    def download(self, **kwargs):
        self.file_manager.new_dir()
        docs = UmvDocument.query_docs(fetch_file_blob=True, **kwargs)

        logger.debug("downloading start")
        for doc in docs:
            file_name_unique = "_".join([str(doc["umvdcm"]), doc["file_name"].replace("/", "")])
            with open(self.file_manager.last_created_dir / file_name_unique, "xb") as file:
                file.write(doc["file_data"])
        logger.debug("downloading finished")
