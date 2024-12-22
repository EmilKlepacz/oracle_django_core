from datetime import datetime

import pytest

from oradja.management.commands.download import parse_date_arg
from django.core.management import CommandError


def test_parse_date_arg_success():
    valid_date_str = "01-02-2020"

    parsed_date = parse_date_arg(valid_date_str)

    assert parsed_date == datetime.strptime(valid_date_str, "%d-%m-%Y").date(), "invalid date"


def test_parse_date_arg_fail():
    invalid_date_str = "2020-02-01"

    with pytest.raises(CommandError, match=f"{invalid_date_str} is not a valid date dd-mm-yyyy"):
        parse_date_arg(invalid_date_str)
