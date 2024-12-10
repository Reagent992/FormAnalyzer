import asyncio

from httpx import AsyncClient

from main import app
from tests.fixtures.forms import test_cases_generator
from tests.test_integration import ASGITransport


async def run_test_queries() -> None:
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    async with AsyncClient(
        base_url="http://localhost",
        transport=ASGITransport(app=app),
    ) as client:
        for input_data, expected_result in test_cases_generator():
            print("### SEND REQUEST ###")
            print(input_data)
            print("### EXPECTED RESULT ###")
            print(expected_result)
            response = await client.post(
                "/get_form",
                content=input_data,
                headers=headers,
            )
            print("### GOT RESULT ###")
            print(response.json())
            print("### CHECK RESULT ###")
            print(response.json() == expected_result)
            print("####################")


if __name__ == "__main__":
    asyncio.run(run_test_queries())
