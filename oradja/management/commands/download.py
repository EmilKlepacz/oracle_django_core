from datetime import datetime

from django.core.management import BaseCommand, CommandError

from oradja.db.docs.doc_processor import DocProcessor
from oradja.file_manager.file_manager import FileManager

_DEFAULT_ROOT_DIR_NAME = "downloads"
_DEFAULT_LIMIT = 3


def parse_date_arg(date_str):
    """Parse a string into a datetime object."""
    try:
        return datetime.strptime(date_str, "%d-%m-%Y").date()
    except ValueError:
        raise CommandError(f"{date_str} is not a valid date dd-mm-yyyy")


class Command(BaseCommand):
    help = "Runs the DocProcessor to download files with optional arguments"

    def add_arguments(self, parser):
        parser.add_argument(
            "--root_dir_name",
            type=str,
            default=_DEFAULT_ROOT_DIR_NAME,
            help=f"Root directory name for downloads. Default value: {_DEFAULT_ROOT_DIR_NAME}"
        )
        parser.add_argument(
            "--new_dir_name",
            default=None,
            type=str,
            help=f"Directory for downloads set. Default value: auto generated %Y-%m-%d_%H-%M-%S"
        )
        parser.add_argument(
            "--created_dati_from",
            default=None,
            type=str,  # Change to string to handle date format
            help="Start date to filter documents from (format: DD-MM-YYYY)"
        )
        parser.add_argument(
            "--created_dati_to",
            default=None,
            type=str,  # Change to string to handle date format
            help="End date to filter documents until (format: DD-MM-YYYY)"
        )
        parser.add_argument(
            "--limit",
            default=_DEFAULT_LIMIT,
            type=int,
            help=f"Limit the number of documents to download. Default value: {_DEFAULT_LIMIT}"
        )
        parser.add_argument(
            "--ids",
            default=None,
            nargs="+",  # This means the argument can take one or more values
            type=int,
            help="List of document IDs"
        )

    def handle(self, *args, **options):
        file_manager = FileManager(options["root_dir_name"],
                                   options["new_dir_name"])
        doc_processor = DocProcessor(file_manager)
        doc_processor.download(**options)
