from enum import Enum, member


class FileType(Enum):
    ASF = "asf"
    AVI = "avi"
    BMP = "bmp"
    CSV = "csv"
    DOC = "doc"
    DOCX = "docx"
    GIF = "gif"
    JPEG = "jpeg"
    JPG = "jpg"
    MOV = "mov"
    MP4 = "mp4"
    MPG = "mpg"
    MSG = "msg"
    PDF = "pdf"
    PNG = "png"
    TIF = "tif"
    TIFF = "tiff"
    TXT = "txt"
    WMV = "wmv"
    XLS = "xls"
    XLSM = "xlsm"
    XLSX = "xlsx"
    XML = "xml"

    @classmethod
    def all(cls):
        return [file_type for file_type in cls]
