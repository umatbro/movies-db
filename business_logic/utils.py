from typing import Union
from datetime import date
from dateutil.parser import parse


def read_field(dictionary: dict, key: str) -> Union[str, None]:
    """
    Read field value from dictionary.
    If there is no `key` in `dictionary` or value is equal to `N/A` return `None`

    :param dictionary: container to read from
    :param key: key to look up
    :return: value or None if value is not available
    """
    empty_values = {'N/A', '', 'null', 'None'}
    value = dictionary.get(key, None)
    return value if value not in empty_values else None


def parse_date(date_str: str) -> Union[date, None]:
    try:
        return parse(date_str)
    except TypeError:
        return None
