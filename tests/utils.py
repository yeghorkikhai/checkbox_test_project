from conftest import client


def get_access_token() -> str:
    response = client.post("/users", json={
        "name": "ФОП Джонсонюк Олег",
        "login": "djonsonukboris",
        "password": "1234567890"
    })

    response_data = response.json()

    return response_data['access_token']
