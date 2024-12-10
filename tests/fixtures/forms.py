import json
import random
import string

from tests.fixtures.date_formats import correct_dates_format_test_cases
from tests.fixtures.emails_fixture import correct_emails
from tests.fixtures.phone_numbers import correct_phone_numbers
from urllib.parse import quote


def test_cases_generator() -> list[tuple[str, dict[str, str]]]:
    with open("tests/fixtures/forms_for_db.json", "r") as f:
        data = json.load(f)
    result = []
    for item in data:
        input = []
        expected_result = {"form_name": item["name"]}
        for key, value in item.items():
            if value == "email":
                input.append(f"{key}={quote(random.choice(correct_emails))}")
            elif value == "phone":
                input.append(
                    f"{key}={quote(random.choice(correct_phone_numbers))}"
                )
            elif value == "date":
                input.append(
                    f"{key}={random.choice(correct_dates_format_test_cases)}"
                )
            elif key == "name":
                continue
            else:
                characters = (
                    string.ascii_letters + string.digits + string.whitespace
                )
                random_string = "".join(random.choices(characters, k=10))
                input.append(f"{key}={random_string}")

        result.append(("&".join(input), expected_result))
    return result
