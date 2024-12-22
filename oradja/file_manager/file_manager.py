import os
from datetime import datetime
from pathlib import Path


def default_dir_name():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


class FileManager:
    def __init__(self, root=None):
        self.root = Path(os.path.abspath(os.curdir)) / root if root else Path(os.path.abspath(os.curdir))
        self.last_created_dir = None

    def new_dir(self, name=None):
        dir_name = name if name else default_dir_name()

        full_path = self.root / dir_name

        os.makedirs(full_path, exist_ok=True)

        self.last_created_dir = full_path

        return full_path
