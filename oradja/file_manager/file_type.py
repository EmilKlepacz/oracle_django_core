from enum import Enum


class FileType(Enum):
    ASF = ("asf", False)
    AVI = ("avi", False)
    BMP = ("bmp", True)
    CSV = ("csv", False)
    DOC = ("doc", True)
    DOCX = ("docx", False)
    GIF = ("gif", True)
    JPEG = ("jpeg", True)
    JPG = ("jpg", True)
    MOV = ("mov", False)
    MP4 = ("mp4", False)
    MPG = ("mpg", False)
    MSG = ("msg", False)
    PDF = ("pdf", True)
    PNG = ("png", True)
    TIF = ("tif", False)
    TIFF = ("tiff", True)
    TXT = ("txt", True)
    WMV = ("wmv", False)
    XLS = ("xls", False)
    XLSM = ("xlsm", False)
    XLSX = ("xlsx", True)
    XML = ("xml", False)

    def __init__(self, value, has_pymupdf_support):
        self._value_ = value
        self.has_pymupdf_support = has_pymupdf_support

    @classmethod
    def all(cls):
        return [file_type for file_type in cls]

    @classmethod
    def get_by_value(cls, value):
        for file_type in cls:
            if file_type.value == value.lower():
                return file_type
        raise ValueError(f"No FileType with value '{value}' found.")
