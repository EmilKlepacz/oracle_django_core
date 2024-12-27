from datetime import date

import pytest

from oradja.db.docs.doc_processor import DocProcessor, download_file_name
from oradja.file_manager.file_manager import FileManager
from oradja.file_manager.file_type import FileType
from oradja.models import ApiUser, UmvDocument


@pytest.mark.parametrize(
    "doc, expected",
    [
        ({"umvdcm": 12345, "file_name": "test_file.txt"}, "12345_test_file.txt"),
        ({"umvdcm": 67890, "file_name": "file/with/slash"}, "67890_filewithslash"),
        ({"umvdcm": 99999, "file_name": ""}, "99999_"),  # Edge case: empty file name
    ],
)
def test_download_file_name(doc, expected):
    result = download_file_name(doc)
    assert result == expected, f"Expected '{expected}', got '{result}'"


@pytest.mark.django_db
def test_download_success(tmp_path):
    api_user = ApiUser.objects.get(name="api")

    doc1 = UmvDocument.objects.create(
        file_name="test1.pdf",
        file_data=b"Simple binary data",
        created_dati=date.today(),
        internal=False,
        notes="This is a test document.",
        apiusr=api_user,
    )
    doc1.save()

    doc2 = UmvDocument.objects.create(
        file_name="test2.pdf",
        file_data=b"Simple binary data",
        created_dati=date.today(),
        internal=False,
        notes="This is a test document.",
        apiusr=api_user,
    )
    doc2.save()

    root_dir_name = tmp_path / "custom_downloads_test"
    new_dir_name = "new_dir"
    file_manager = FileManager(root_dir_name=root_dir_name, new_dir_name=new_dir_name)

    doc_processor = DocProcessor(file_manager=file_manager)

    doc_processor.download(ids=[doc1.umvdcm, doc2.umvdcm])

    assert file_manager.last_created_dir_path == file_manager.root_dir_path / new_dir_name, f"last_created_dir is not correct."

    doc1_path = root_dir_name / new_dir_name / "_".join([str(doc1.umvdcm), str(doc1.file_name)])
    doc2_path = root_dir_name / new_dir_name / "_".join([str(doc2.umvdcm), str(doc2.file_name)])
    assert doc1_path.is_file(), f"Missing download file: {doc1_path}"
    assert doc2_path.is_file(), f"Missing download file: {doc2_path}"


def test_set_file_types_with_not_the_list_throws_value_error():
    file_manager = FileManager()
    doc_processor = DocProcessor(file_manager=file_manager)

    with pytest.raises(ValueError):
        doc_processor.file_types = FileType.PDF

def test_set_file_types_with_not_file_type_enum_throws_value_error():
    file_manager = FileManager()
    doc_processor = DocProcessor(file_manager=file_manager)

    with pytest.raises(ValueError):
        doc_processor.file_types = "some_test_extension"
