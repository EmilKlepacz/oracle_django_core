from datetime import date, datetime
from typing import Optional, List, Union


class RequestParamsParser:

    @staticmethod
    def parse(val: Optional[str],
              type_: type = int,
              list_type: type = None) -> Optional[Union[int, date, List[int], List[str]]]:
        if not val:
            return None

        if type_ == int:
            return int(val)
        elif type_ == date:
            return datetime.strptime(val, "%d-%m-%Y").date()
        elif type_ == list:
            if list_type is None:
                raise ValueError("list_type must be specified")

            if list_type == int:
                return [int(item.strip()) for item in val.split(",")]
            elif list_type == str:
                return [item.strip() for item in val.split(",")]
        else:
            raise ValueError(f"Unsupported type: {type_}")
