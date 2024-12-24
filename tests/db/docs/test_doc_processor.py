from datetime import date

import pytest

from oradja.db.docs.doc_processor import DocProcessor
from oradja.file_manager.file_manager import FileManager
from oradja.models import ApiUser, UmvDocument


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
