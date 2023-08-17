import pytest
from conftest import client


def get_access_token() -> str:
    response = client.post("/users", json={
        "name": "ФОП Джонсонюк Олег",
        "login": "djonsonukboris",
        "password": "1234567890"
    })

    response_data = response.json()

    return response_data['access_token']


access_token = get_access_token()

headers = {
    "authorization": f"Bearer {access_token}"
}


def test_registration():
    response = client.post("/users", json={
        "name": "ФОП Джонсонюк Борис Олексійович",
        "login": "djonsonuk",
        "password": "1234567890"
    })

    assert response.status_code == 200, "User can\'t be register"


def test_registration_without_password():
    # try register user without password
    response = client.post("/users", json={
        "name": "ФОП Джонсонюк Борис Олексійович",
        "login": "djonsonuk"
    })

    assert response.status_code == 422


def test_registration_too_long_login():
    # try register user with too long login
    response = client.post("/users", json={
        "name": "ФОП Джонсонюк Борис Олексійович",
        "login": "djonsonukborisolksiyovichdjonsonukborisolksiyovich",
        "password": "1234567890"
    })

    assert response.status_code == 422


# Test user auth
def test_user_authorization():
    response = client.get(
        url="/users/me",
        headers=headers
    )

    assert response.status_code == 200


def test_user_authorization_without_key():
    response = client.get(url="/users/me")

    assert response.status_code == 403
