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


# Create receipt Tests
def test_create_receipt():
    response = client.post(
        url="/receipts",
        headers=headers,
        json={
            "products": [
                {
                    "name": "Some Product",
                    "price": 100,
                    "quantity": 1
                }
            ],
            "payment": {
                "type": "CASH",
                "amount": 100
            }
        }
    )

    assert response.status_code == 200


def test_create_receipt_without_products():
    response = client.post(
        url="/receipts",
        headers=headers,
        json={
            "payment": {
                "type": "CASH",
                "amount": 100
            }
        }
    )

    assert response.status_code == 422


def test_create_receipt_with_empty_list_of_products():
    response = client.post(
        url="/receipts",
        headers=headers,
        json={
            "products": [],
            "payment": {
                "type": "CASH",
                "amount": 100
            }
        }
    )

    assert response.status_code == 422


def test_create_receipt_with_negative_amount():
    response = client.post(
        url="/receipts",
        headers=headers,
        json={
            "products": [
                {
                    "name": "Some Product",
                    "price": 100,
                    "quantity": 1
                }
            ],
            "payment": {
                "type": "CASH",
                "amount": -100
            }
        }
    )

    assert response.status_code == 422


def test_create_receipt_with_product_with_negative_amount():
    response = client.post(
        url="/receipts",
        headers=headers,
        json={
            "products": [
                {
                    "name": "Some Product",
                    "price": -100,
                    "quantity": 1
                }
            ],
            "payment": {
                "type": "CASH",
                "amount": 100
            }
        }
    )

    assert response.status_code == 422


# Get receipts Tests
def test_get_receipts():
    response = client.get(
        url="/receipts",
        headers=headers
    )

    assert response.status_code == 200


def test_get_receipts_with_negative_limit():
    response = client.get(
        url="/receipts",
        headers=headers,
        params={
            "limit": -10
        }
    )

    assert response.status_code == 422


def test_get_receipts_with_grate_limit():
    response = client.get(
        url="/receipts",
        headers=headers,
        params={
            "limit": 1000
        }
    )

    assert response.status_code == 422


def test_get_receipts_with_negative_offset():
    response = client.get(
        url="/receipts",
        headers=headers,
        params={
            "offset": -1
        }
    )

    assert response.status_code == 422


# Search receipts Tests

# Get text receipt without auth Tests
def test_get_text_receipt():
    response = client.get(url="/receipts/1")

    assert response.status_code == 200


def test_get_text_receipt_with_width_60():
    response = client.get(
        url="/receipts/1",
        params={
            "width": 60
        }
    )

    assert response.status_code == 200


def test_get_text_receipt_with_width_less_min():
    response = client.get(
        url="/receipts/1",
        params={
            "width": 1
        }
    )

    assert response.status_code == 422


def test_get_text_receipt_with_width_grate_max():
    response = client.get(
        url="/receipts/1",
        params={
            "width": 1000
        }
    )

    assert response.status_code == 422
