from pathlib import Path
from unittest.mock import patch, MagicMock

from oradja.db.docs.doc_extractor import DocExtractor
from oradja.file_manager.file_type import FileType
import pytest


@pytest.fixture
def doc_extractor():
    return DocExtractor(FileType.PDF)


@patch("pymupdf.open")
@pytest.mark.parametrize(
    "encoding",
    [
        "utf-8",
        "iso-8859-1"
    ],
)
def test_extracts_pdf_with_text_to_json(mock_pymupdf_open, doc_extractor, encoding):
    mock_doc = MagicMock()

    # Create multiple mock pages with unique content
    mock_page_1 = MagicMock()
    mock_page_1.get_text.side_effect = [
        "Page with text 1",  # Plain text content for page 1
        '{"key": "value_1"}',  # JSON content for page 1
    ]
    mock_page_2 = MagicMock()
    mock_page_2.get_text.side_effect = [
        "Page with text 2",  # Plain text content for page 2
        '{"key": "value_2"}',  # JSON content for page 2
    ]
    mock_doc.__iter__.return_value = [mock_page_1, mock_page_2]

    mock_pymupdf_open.return_value = mock_doc

    result = doc_extractor.extract_to_json(Path("fake_path.pdf"), encoding=encoding)

    assert "pages" in result, "'pages' is key missing"
    assert len(result["pages"]) == 2, "result should have 2 pages"
    assert result["pages"][0]["page_number"] == 1, "Page number should be 1"
    assert result["pages"][0]["content"]["key"] == "value_1", "Content of the first page should match"
    assert result["pages"][1]["page_number"] == 2, "Page number should be 2"
    assert result["pages"][1]["content"]["key"] == "value_2", "Content of the first page should match"


def test_doc_extractor_init_for_file_type_not_supported_by_pymupdf():
    not_supported_file_type = FileType.AVI

    with pytest.raises(ValueError, match=f"No pymupdf support for {not_supported_file_type.name}"):
        doc_extractor = DocExtractor(FileType.AVI)
