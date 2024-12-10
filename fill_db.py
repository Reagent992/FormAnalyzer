import asyncio
import json

from main import get_db


async def fill_db():
    collection = get_db()
    with open("tests/fixtures/forms_for_db.json", "r") as f:
        data = json.load(f)
    await collection.insert_many(data)


if __name__ == "__main__":
    asyncio.run(fill_db())