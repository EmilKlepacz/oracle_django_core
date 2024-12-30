import os
import re
from datetime import datetime
from pathlib import Path
import pytest

from oradja.file_manager.file_manager import FileManager, default_dir_name
from oradja.models import ApiModProperty


@pytest.mark.django_db
def test_default_dir_name_returns_correct_file_name():
    file_name_regex = r"^.*_\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}$"
    assert re.match(file_name_regex,
                    default_dir_name()), f"Directory name {default_dir_name} does not match the expected format"


def test_new_dir_creates_directory_with_name(tmp_path):
    root_dir_name = tmp_path / "custom_downloads"
    new_dir_name = "new_dir"

    file_manager = FileManager(root_dir_name=root_dir_name, new_dir_name="new_dir")
    file_manager.new_dir()

    created_dir_path = Path(root_dir_name) / new_dir_name

    assert created_dir_path.is_dir(), f"Directory {created_dir_path} was not created"


@pytest.mark.django_db
def test_new_dir_creates_directory_with_default_current_date_based_name(tmp_path):
    root_dir_name = tmp_path / "custom_downloads"
    file_manager = FileManager(root_dir_name=root_dir_name)

    full_path = file_manager.new_dir()  # leave argument empty to get default name in format %Y-%m-%d_%H-%M-%S

    assert full_path.is_dir(), f"Directory {full_path} was not created"

    file_name_regex = r"^.*_\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}$"
    assert re.match(file_name_regex, full_path.name), f"Directory name {full_path} does not match the expected format"


def test_file_manager_creates_dir_under_custom_download_root(tmp_path):
    root_dir_name = tmp_path / "custom_downloads"
    new_dir_name = "new_dir"
    file_manager = FileManager(root_dir_name=root_dir_name, new_dir_name=new_dir_name)

    file_manager.new_dir()

    assert (Path(os.path.abspath(os.curdir)) / root_dir_name / new_dir_name).is_dir(), \
        f"Directory {Path(os.path.abspath(os.curdir)) / root_dir_name / new_dir_name} was not created"


def test_file_manager_set_last_created_dir_correctly(tmp_path):
    root_dir_name = tmp_path / "custom_downloads"

    new_dir_name_1 = "test_dir_1"
    file_manager = FileManager(root_dir_name=root_dir_name, new_dir_name=new_dir_name_1)
    file_manager.new_dir()

    assert file_manager.last_created_dir_path == file_manager.root_dir_path / new_dir_name_1, f"last_created_dir is not correct."

    new_dir_name_2 = "test_dir_2"
    file_manager = FileManager(root_dir_name=root_dir_name, new_dir_name=new_dir_name_2)
    file_manager.new_dir()

    assert file_manager.last_created_dir_path == file_manager.root_dir_path / new_dir_name_2, f"last_created_dir is not correct."
