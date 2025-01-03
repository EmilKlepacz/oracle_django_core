import json
from pathlib import Path
from typing import Dict, Callable

import pymupdf

from oradja.file_manager.file_type import FileType


class DocExtractor:
    def __init__(self, file_type: FileType):
        if not file_type.has_pymupdf_support:
            raise ValueError(f'No pymupdf support for {file_type.name}')
        self.file_type = file_type

    def extract_to_json(self, doc_path: Path, encoding: str = "utf-8") -> dict:
        file_handlers: Dict[FileType, Callable[[Path, str], dict]] = {
            FileType.PDF: self._handle_pdf,
            FileType.BMP: self._handle_bmp,
            FileType.JPEG: self._handle_jpeg,
            FileType.DOC: self._handle_doc,
            FileType.GIF: self._handle_gif,
            FileType.JPG: self._handle_jpg,
            FileType.PNG: self._handle_png,
            FileType.TIFF: self._handle_tiff,
            FileType.TXT: self._handle_txt,
            FileType.XLSX: self._handle_xlsx,
        }

        handler = file_handlers.get(self.file_type)
        return handler(doc_path, encoding)

    def _handle_pdf(self, doc_path: Path, encoding: str) -> dict:
        doc = pymupdf.open(doc_path)
        has_text = False

        pages = []
        page_num = 0
        for page in doc:
            # Check if the page contains any selectable text
            # in other case it is probably a scan (image only)
            if page.get_text("text").strip():
                has_text = True  # Document has selectable text

            # Get the raw JSON string in UTF-8 by default
            page_raw_json = page.get_text("json")

            if encoding.lower() != "utf-8":
                page_raw_json = page_raw_json.encode("utf-8").decode(encoding=encoding, errors="replace")

            page_json = json.loads(page_raw_json)

            pages.append({
                "page_number": page_num + 1,
                "content": page_json,
            })
            page_num += 1

        # If no selectable text was found
        # (it is a scan so here some OCR needs to be used)
        if not has_text:
            # todo OCR logic to implement...
            pass

        pages_json = {"pages": pages}
        return pages_json

    def _handle_bmp(self, doc_path: Path, encoding: str = "utf-8") -> dict:
        return {}

    def _handle_jpeg(self, doc_path: Path, encoding: str = "utf-8") -> dict:
        return {}

    def _handle_doc(self, doc_path: Path, encoding: str = "utf-8") -> dict:
        return {}

    def _handle_gif(self, doc_path: Path, encoding: str = "utf-8") -> dict:
        return {}

    def _handle_jpg(self, doc_path: Path, encoding: str = "utf-8") -> dict:
        return {}

    def _handle_png(self, doc_path: Path, encoding: str = "utf-8") -> dict:
        return {}

    def _handle_tiff(self, doc_path: Path, encoding: str = "utf-8") -> dict:
        return {}

    def _handle_txt(self, doc_path: Path, encoding: str = "utf-8") -> dict:
        return {}

    def _handle_xlsx(self, doc_path: Path, encoding: str = "utf-8") -> dict:
        return {}
