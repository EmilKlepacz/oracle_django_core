import os
from datetime import datetime
from pathlib import Path

from oradja.models import ApiModProperty


def default_dir_name():
    env = ApiModProperty.objects.get(name="name").value
    return "_".join([env, datetime.now().strftime("%Y-%m-%d_%H-%M-%S")])


class FileManager:
    def __init__(self, root_dir_name=None, new_dir_name=None):
        self._root_dir_name = root_dir_name
        self._new_dir_name = new_dir_name
        self._last_created_dir_path = None

    @property
    def root_dir_name(self):
        return self._root_dir_name

    @root_dir_name.setter
    def root_dir_name(self, value):
        self._root_dir_name = value

    @property
    def root_dir_path(self):
        return Path(os.path.abspath(os.curdir)) / self.root_dir_name if self.root_dir_name else Path(
            os.path.abspath(os.curdir))

    @property
    def new_dir_name(self):
        return self._new_dir_name if self._new_dir_name else default_dir_name()

    @new_dir_name.setter
    def new_dir_name(self, value):
        self._new_dir_name = value

    @property
    def last_created_dir_path(self):
        return self._last_created_dir_path

    @last_created_dir_path.setter
    def last_created_dir_path(self, value):
        self._last_created_dir_path = value

    def new_dir(self):
        full_path = self.root_dir_path / self.new_dir_name
        os.makedirs(full_path, exist_ok=True)
        self.last_created_dir_path = full_path
        return full_path
