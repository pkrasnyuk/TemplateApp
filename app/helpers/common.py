from datetime import date, datetime
from typing import Any

import pytz


def defaut_epsilon() -> float:
    return 1e-6


def default_float_digits() -> int:
    return 4


def defaut_float_format() -> str:
    return "{:." + str(default_float_digits()) + "f}"


def default_date_format() -> str:
    return "%Y-%m-%d"


def defaut_string_length() -> int:
    return 10


def generate_datetime(year: int, month: int, day: int) -> datetime:
    return datetime(
        year=year,
        month=month,
        day=day,
        tzinfo=pytz.timezone("UTC"),
    )


def min_datetime() -> datetime:
    return generate_datetime(year=1900, month=1, day=1)


def reduced_string(string: str, length: int) -> str:
    reduced = string[0:length]
    reduced_length = len(reduced) - 3
    return reduced[0:reduced_length] + "..." if reduced_length > 0 else reduced


def value2str(
    value: Any,
    epsilon: float = defaut_epsilon(),
    float_format=defaut_float_format(),
    date_format=default_date_format(),
    string_length: int = defaut_string_length(),
) -> str:
    if value is None:
        return ""
    elif isinstance(value, str):
        return value if len(value) <= string_length else reduced_string(value, string_length)
    elif isinstance(value, float):
        return float_format.format(value) if (abs(value) > epsilon) else float_format.format(0.0)
    elif isinstance(value, (date, datetime)):
        return value.strftime(date_format)
    elif isinstance(value, int):
        return str(value)
    else:
        return ""


def default_json_dumps(value: Any) -> Any:
    return value2str(value=value)


def date2datetime(dt: date) -> datetime:
    return generate_datetime(year=dt.year, month=dt.month, day=dt.day)


def is_value_empty(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str) and value == "":
        return True
    if isinstance(value, float) and abs(value) < defaut_epsilon():
        return True
    if isinstance(value, datetime) and value < min_datetime():
        return True
    if isinstance(value, date) and date2datetime(value) < min_datetime():
        return True
    if isinstance(value, int) and value == 0:
        return True
    return False
