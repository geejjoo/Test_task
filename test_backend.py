import pytest
import requests

BASE_URL = "https://host:80"


@pytest.fixture
def base_url():
    return BASE_URL


@pytest.fixture
def user_name():
    return "TestUser"


@pytest.fixture
def user_id(base_url, user_name):
    create_user_response = requests.post(
        f"{base_url}/CreateUser", json={"Name": user_name}
    )
    assert create_user_response.status_code == 201
    user_id = create_user_response.json()["id"]
    return user_id


def test_create_user(base_url):
    user_name = "TestCreationUser"
    create_user_response = requests.post(
        f"{base_url}/CreateUser", json={"Name": user_name}
    )
    assert create_user_response.status_code == 201
    user_id = create_user_response.json()["id"]

    get_user_response = requests.get(f"{base_url}/GetUser", json={"id": user_id})
    assert get_user_response.status_code == 200
    assert get_user_response.json()["Name"] == user_name


@pytest.mark.parametrize("user_id", [
    999999,
    "abc",
    "",
])
def test_get_unexisting_user(base_url, user_id):
    get_user_response = requests.get(f"{base_url}/GetUser", json={"id": user_id})
    assert get_user_response.status_code == 404


def test_set_user_age(base_url, user_name, user_id):
    user_age = 30

    set_age_response = requests.post(f"{base_url}/SetUserAge", json={"id": user_id, "Age": user_age})
    assert set_age_response.status_code == 200

    get_user_response = requests.get(f"{base_url}/GetUser", json={"id": user_id})
    assert get_user_response.status_code == 200
    assert get_user_response.json()["Name"] == user_name
    assert get_user_response.json()["Age"] == user_age


@pytest.mark.parametrize("age", [
    -1,
    101,
    "abc",
    "",
])
def test_set_user_unexpected_age(base_url, user_id, age):
    data = {"id": user_id, "Age": age}
    set_age_response = requests.post(f"{base_url}/SetUserAge", json=data)

    assert set_age_response.status_code == 400


@pytest.mark.parametrize("age,expected_group", [
    (0, "Young"),
    (18, "Young"),
    (19, "Adult"),
    (100, "Adult"),
])
def test_age_group(base_url, user_id, age, expected_group):
    data = {"id": user_id, "Age": age}
    set_age_response = requests.post(f"{base_url}/SetUserAge", json=data)

    assert set_age_response.status_code == 200

    get_group_response = requests.get(f"{base_url}/{user_id}/GetAgeGroupById")

    assert get_group_response.status_code == 200
    assert get_group_response.json()["AgeGroup"] == expected_group
