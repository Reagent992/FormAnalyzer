import pytest
from tests.fixtures.date_formats import (
    correct_dates_format_test_cases,
    invalid_dates_format_test_cases,
)
from tests.fixtures.phone_numbers import (
    correct_phone_numbers,
    wrong_numbers,
)

from main import validate_and_parse_data
from tests.fixtures.emails_fixture import correct_emails, invalid_emails
from validators import validate_date, validate_email, validate_phone


@pytest.mark.parametrize("phone", correct_phone_numbers)
def test_validate_correct_phone_numbers(phone: str) -> None:
    """Check that phone is validated."""
    assert validate_phone(phone)


@pytest.mark.parametrize("phone", wrong_numbers)
def test_validate_wrong_phone_numbers(phone: str) -> None:
    """Check that phone is validated."""
    assert not validate_phone(phone)


@pytest.mark.parametrize("correct_email", correct_emails)
def test_validate_correct_emails(correct_email: str) -> None:
    assert validate_email(correct_email)  is True


@pytest.mark.parametrize("invalid_email", invalid_emails)
def test_validate_wrong_emails(invalid_email: str) -> None:
    assert not validate_email(invalid_email)


@pytest.mark.parametrize("date_type", correct_dates_format_test_cases)
def test_correct_date_validation(date_type):
    assert validate_date(date_type)


@pytest.mark.parametrize("date_type", invalid_dates_format_test_cases)
def test_invalid_date_validation(date_type):
    assert not validate_date(date_type)


@pytest.mark.asyncio
async def test_validate_and_parse_data_with_date():
    data = {"date_field": "1-1-2022"}
    expected_result = {"date_field": "date"}
    result = await validate_and_parse_data(data)
    assert result == expected_result


@pytest.mark.asyncio
async def test_validate_and_parse_data_with_phone():
    data = {"phone_field": "+79999999999"}
    expected_result = {"phone_field": "phone"}
    result = await validate_and_parse_data(data)
    assert result == expected_result


@pytest.mark.asyncio
async def test_validate_and_parse_data_with_email():
    data = {"email_field": "example@example.com"}
    expected_result = {"email_field": "email"}
    result = await validate_and_parse_data(data)
    assert result == expected_result


@pytest.mark.asyncio
async def test_validate_and_parse_data_with_unknown_type():
    data = {"unknown_field": "some_value"}
    expected_result = {"unknown_field": "text"}
    result = await validate_and_parse_data(data)
    assert result == expected_result


@pytest.mark.asyncio
async def test_validate_and_parse_data_with_multiple_fields():
    data = {
        "date_field": "2022-01-01",
        "phone_field": "+79999999999",
        "email_field": "example@example.com",
        "unknown_field": "some_value",
    }
    expected_result = {
        "date_field": "date",
        "phone_field": "phone",
        "email_field": "email",
        "unknown_field": "text",
    }
    result = await validate_and_parse_data(data)
    assert result == expected_result
