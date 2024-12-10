import json
import uuid

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

from main import app, get_db
from tests.fixtures.forms import test_cases_generator

"""
This is an integration test that requires a real database to run.
"""

DB_NAME = uuid.uuid4().hex
DB_COLLECTION_NAME = uuid.uuid4().hex


@pytest_asyncio.fixture(scope="module", autouse=True)
async def db_collection():
    """
    Creates a new DB with a collection from data in json file.
    After the test is finished, it drops the database.
    """
    client = AsyncIOMotorClient()  # type: ignore
    db = client[DB_NAME]
    collection = db[DB_COLLECTION_NAME]
    with open("tests/fixtures/forms_for_db.json", "r") as f:
        data = json.load(f)
    await collection.insert_many(data)
    yield collection
    await client.drop_database(db.name)


@pytest.fixture(scope="module", autouse=True)
def override_get_db(db_collection):
    """Overrides the get_db function to use the temporary test db."""

    def _get_db():
        return AsyncIOMotorClient()[DB_NAME][DB_COLLECTION_NAME]

    app.dependency_overrides[get_db] = _get_db
    yield
    app.dependency_overrides.clear()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_data, expected_response", test_cases_generator()
)
async def test_get_form(
    input_data: str,
    expected_response: str,
) -> None:
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    async with AsyncClient(
        base_url="http://localhost", transport=ASGITransport(app=app)
    ) as client:
        result = await client.post(
            "/get_form",
            content=input_data,
            headers=headers,
        )
        assert result.json() == expected_response
