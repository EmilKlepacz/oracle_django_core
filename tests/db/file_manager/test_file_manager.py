import os
import re
from datetime import datetime
from pathlib import Path

from oradja.file_manager.file_manager import FileManager, default_dir_name


def test_default_dir_name_returns_correct_file_name():
    name_current_date_based = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    assert default_dir_name() == name_current_date_based, f"Default new dir name should be equal to {default_dir_name}"


def test_new_dir_creates_directory_with_name(tmp_path):
    custom_root = tmp_path / "test_downloads_dir"
    file_manager = FileManager(root=custom_root)

    dir_name = "test_dir"
    file_manager.new_dir(dir_name)

    created_dir = Path(custom_root) / dir_name

    assert created_dir.is_dir(), f"Directory {created_dir} was not created"


def test_new_dir_creates_directory_with_default_current_date_based_name(tmp_path):
    custom_root = tmp_path / "test_downloads_dir"
    file_manager = FileManager(root=custom_root)

    full_path = file_manager.new_dir()  # leave argument empty to get default name in format %Y-%m-%d_%H-%M-%S

    assert full_path.is_dir(), f"Directory {full_path} was not created"

    date_regex = r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}$"
    assert re.match(date_regex, full_path.name), f"Directory name {full_path} does not match the expected format"


def test_file_manager_creates_dir_under_custom_download_root(tmp_path):
    custom_root = tmp_path / "test_downloads_dir"
    file_manager = FileManager(root=custom_root)

    dir_name = "test_dir"
    file_manager.new_dir(dir_name)

    assert (Path(os.path.abspath(os.curdir)) / custom_root / dir_name).is_dir(), \
        f"Directory {Path(os.path.abspath(os.curdir)) / custom_root / dir_name} was not created"


def test_file_manager_set_last_created_dir_correctly(tmp_path):
    custom_root = tmp_path / "test_downloads_dir"
    file_manager = FileManager(root=custom_root)

    dir_name_1 = "test_dir_1"
    file_manager.new_dir(dir_name_1)

    assert file_manager.last_created_dir == file_manager.root / dir_name_1, f"last_created_dir is not correct."

    dir_name_2 = "test_dir_2"
    file_manager.new_dir(dir_name_2)

    assert file_manager.last_created_dir == file_manager.root / dir_name_2, f"last_created_dir is not correct."
