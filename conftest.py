import pytest
import requests
import helpers


BASE_URL = "https://qa-scooter.praktikum-services.ru"


@pytest.fixture
def create_courier():
    """Фикстура: создаёт курьера и удаляет после теста"""
    login_pass = helpers.register_new_courier_and_return_login_password()
    yield login_pass
    # Удаляем курьера после теста
    if login_pass:
        login = login_pass[0]
        password = login_pass[1]
        # Получаем id курьера
        login_response = requests.post(
            f"{BASE_URL}/api/v1/courier/login",
            data={"login": login, "password": password}
        )
        if login_response.status_code == 200:
            courier_id = login_response.json()["id"]
            requests.delete(f"{BASE_URL}/api/v1/courier/{courier_id}")