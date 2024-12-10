import re
from datetime import datetime

from email_validator import (
    EmailNotValidError,
)
from email_validator import (
    validate_email as validate_email_lib,
)
from fastapi.datastructures import FormData

from config import DATE_FORMAT_PATTERNS, REGEX_PHONE_PATTERN


def validate_email(email: str) -> bool:
    try:
        validate_email_lib(email, check_deliverability=False)
        return True
    except EmailNotValidError:
        return False


def validate_phone(phone: str) -> bool:
    if re.match(REGEX_PHONE_PATTERN, phone):
        return True
    return False


def normalize_date(date_str: str) -> str:
    return re.sub(r"[\.\/\-:,]", ".", date_str)


def validate_date(date_str: str) -> bool:
    for date_format_pattern in DATE_FORMAT_PATTERNS:
        try:
            datetime.strptime(normalize_date(date_str), date_format_pattern)
            return True
        except ValueError:
            continue
    return False


def formdata_to_str_dict(formdata: FormData) -> dict[str, str]:
    return {
        key: value for key, value in formdata.items() if isinstance(value, str)
    }
