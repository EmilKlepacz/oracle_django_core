import re
from datetime import datetime
from pathlib import Path

from oradja.db.file_manager.file_manager import FileManager, default_dir_name


def test_default_dir_name_returns_correct_file_name():
    name_current_date_based = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    assert default_dir_name() == name_current_date_based, f"Default new dir name should be equal to {default_dir_name}"


def test_new_dir_creates_directory_with_name(tmp_path):
    root = "test_downloads_dir"
    file_manager = FileManager(root=root)

    dir_name = "test_dir"
    file_manager._new_dir(dir_name)

    created_dir = Path(root) / dir_name

    assert created_dir.is_dir(), f"Directory {created_dir} was not created"


def test_new_dir_creates_directory_with_default_current_date_based_name(tmp_path):
    root = "test_downloads_dir"
    file_manager = FileManager(root=root)

    full_path = file_manager._new_dir()  # leave argument empty to get default name in format %Y-%m-%d_%H-%M-%S

    assert full_path.is_dir(), f"Directory {full_path} was not created"

    date_regex = r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}$"
    assert re.match(date_regex, full_path.name), f"Directory name {full_path} does not match the expected format"
