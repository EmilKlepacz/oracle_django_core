from oradja.file_manager.file_manager import FileManager
from oradja.models import UmvDocument


class DocProcessor:
    def __init__(self, file_manager: FileManager):
        self.file_manager = file_manager

    def download(self, **kwargs):
        self.file_manager.new_dir()
        docs = UmvDocument.query_docs(fetch_file_blob=True, **kwargs)

        for doc in docs:
            file_name_unique = "_".join([str(doc["umvdcm"]), doc["file_name"]])
            with open(self.file_manager.last_created_dir / file_name_unique, "xb") as file:
                file.write(doc["file_data"])
