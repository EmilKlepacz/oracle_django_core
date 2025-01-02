from oradja.db.docs.doc_extractor import DocExtractor
from oradja.file_manager.file_type import FileType
import pytest


def test_doc_extractor_init_for_file_type_not_supported_by_pymupdf():
    not_supported_file_type = FileType.AVI

    with pytest.raises(ValueError, match=f"No pymupdf support for {not_supported_file_type.name}"):
        doc_extractor = DocExtractor(FileType.AVI)
