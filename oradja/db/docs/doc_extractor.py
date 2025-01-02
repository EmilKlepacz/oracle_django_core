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

    def extract_to_json(self, doc_path: Path) -> dict:
        file_handlers: Dict[FileType, Callable[[Path], dict]] = {
            FileType.PDF: self.handle_pdf,
            FileType.BMP: self.handle_bmp,
            FileType.JPEG: self.handle_jpeg,
            FileType.DOC: self.handle_doc,
            FileType.GIF: self.handle_gif,
            FileType.JPG: self.handle_jpg,
            FileType.PNG: self.handle_png,
            FileType.TIFF: self.handle_tiff,
            FileType.TXT: self.handle_txt,
            FileType.XLSX: self.handle_xlsx,
        }

        handler = file_handlers.get(self.file_type)
        return handler(doc_path)

    def handle_pdf(self, doc_path: Path) -> dict:
        doc = pymupdf.open(doc_path)

        pages = []
        page_num = 0
        for page in doc:
            # Get the raw JSON string in UTF-8
            page_raw_json = page.get_text("json")
            page_json = json.loads(page_raw_json)

            pages.append({
                "page_number": page_num + 1,
                "content": page_json,
            })
            page_num += 1

        pages_json = {"pages": pages}
        return pages_json

    def handle_bmp(self, doc_path: Path) -> dict:
        return {}

    def handle_jpeg(self, doc_path: Path) -> dict:
        return {}

    def handle_doc(self, doc_path: Path) -> dict:
        return {}

    def handle_gif(self, doc_path: Path) -> dict:
        return {}

    def handle_jpg(self, doc_path: Path) -> dict:
        return {}

    def handle_png(self, doc_path: Path) -> dict:
        return {}

    def handle_tiff(self, doc_path: Path) -> dict:
        return {}

    def handle_txt(self, doc_path: Path) -> dict:
        return {}

    def handle_xlsx(self, doc_path: Path) -> dict:
        return {}
