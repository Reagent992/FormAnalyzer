from typing import Annotated, Any, Optional

from fastapi import Depends, FastAPI, Request
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
)

from config import DB_COLLECTION_NAME, DB_NAME
from validators import (
    formdata_to_str_dict,
    validate_date,
    validate_email,
    validate_phone,
)

app = FastAPI()
db_client: AsyncIOMotorClient = AsyncIOMotorClient()


def get_db() -> AsyncIOMotorCollection:
    return db_client[DB_NAME][DB_COLLECTION_NAME]


async def find_appropriate_form(
    fields: dict[str, str],
    get_db: Annotated[AsyncIOMotorCollection, Depends(get_db)],
) -> Optional[dict[str, str]]:
    aggregation_pipeline: list[dict[str, Any]] = [
        {"$match": fields},
        # The first stage is filtering by the passed fields.
        # There may be more than one document,
        # so we need to limit the number of results to one.
        {
            "$addFields": {
                "field_count": {"$size": {"$objectToArray": "$$ROOT"}}
            }
        },
        # Add a new field to document called: field_count
        # it will contain amount of fields in document.
        # $objectToArray returns an array of key-value pairs.
        # $$ROOT is a variable that points to the current document.
        {"$sort": {"field_count": 1}},
        # Sort documents by temporary field: field_count in a ascending order.
        {"$limit": 1},
        # Limit the number of results to one. Because we need
        {"$unset": "field_count"},
        # delete temporary variable: field_count
    ]
    collection = get_db
    result = await collection.aggregate(aggregation_pipeline).to_list()
    return result[0] if result else None


async def validate_and_parse_data(data: dict[str, str]) -> dict[str, str]:
    """Iterate over the passed data and check what type of data it is.

    Because the key is a false data source,
    Keys may be: mail, email, your email, etc.
    All unknown data types are marked as text.

    Returns:
        Processed data dictionary with data types.
    """
    for key, value in data.items():
        if validate_date(value):
            data[key] = "date"
        elif validate_phone(value):
            data[key] = "phone"
        elif validate_email(value):
            data[key] = "email"
        else:
            data[key] = "text"
    return data


@app.post("/get_form")
async def get_form(
    request: Request,
    get_db: Annotated[AsyncIOMotorCollection, Depends(get_db)] = get_db(),
) -> dict[str, str]:
    """
    Endpoint to process form data submitted via POST request.

    The endpoint expects form data (x-www-form-urlencoded)
    in the following format:
        `email=example@example.com&phone=+79999999999`

    Returns:
        - The name of the form if found.
        - Processed data dictionary with data types if no form is found.
    """
    form_data = await request.form()
    form_data_str_dict = formdata_to_str_dict(form_data)
    processed_data = await validate_and_parse_data(form_data_str_dict)
    if form := await find_appropriate_form(form_data_str_dict, get_db):
        return {"form_name": form["name"]}
    return processed_data
