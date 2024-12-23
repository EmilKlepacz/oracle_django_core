import os
from datetime import datetime
from pathlib import Path


def default_dir_name():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


class FileManager:
    def __init__(self, root_dir_name=None, new_dir_name=None):
        self.root_dir_name = Path(os.path.abspath(os.curdir)) / root_dir_name if root_dir_name else Path(os.path.abspath(os.curdir))
        self.last_created_dir = None
        self.new_dir_name = new_dir_name

    def new_dir(self):
        new_dir_name = self.new_dir_name if self.new_dir_name else default_dir_name()

        full_path = self.root_dir_name / new_dir_name

        os.makedirs(full_path, exist_ok=True)

        self.last_created_dir = full_path

        return full_path
