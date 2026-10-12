import pytest
import requests
import allure

from config import COURIER_ENDPOINT
from helpers import (
    generate_random_string,
    create_courier,
    register_new_courier_and_return_login_password,
)


@allure.feature("Создание курьера")
class TestCreateCourier:
    """Тесты для ручки «Создание курьера»"""

    def test_create_courier_success(self, courier):
        """Курьера можно создать"""
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        response = create_courier(login, password, first_name)

        # Добавляем курьера в список для удаления
        courier.append((login, password))

        assert response.status_code == 201
        assert response.json() == {"ok": True}

    def test_create_two_identical_couriers(self, courier):
        """Нельзя создать двух одинаковых курьеров"""
        login_pass = register_new_courier_and_return_login_password()
        login, password, first_name = login_pass
        courier.append((login, password))

        response = create_courier(login, password, first_name)

        assert response.status_code == 409
        assert response.json()["message"] == "Этот логин уже используется. Попробуйте другой."

    @pytest.mark.parametrize("field", ["login", "password"])
    def test_create_courier_without_field(self, field):
        """Чтобы создать курьера, нужно передать все обязательные поля"""
        payload = {
            "login": generate_random_string(10),
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        payload.pop(field)

        response = requests.post(COURIER_ENDPOINT, data=payload)

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"