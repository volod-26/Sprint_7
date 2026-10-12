import pytest
import requests
import allure

from config import COURIER_LOGIN_ENDPOINT
from helpers import (
    register_new_courier_and_return_login_password,
    login_courier,
)


@allure.feature("Логин курьера")
class TestLoginCourier:
    """Тесты для ручки «Логин курьера»"""

    def test_login_courier_success(self, courier):
        """Курьер может авторизоваться"""
        login_pass = register_new_courier_and_return_login_password()
        login, password, first_name = login_pass
        courier.append((login, password))

        response = login_courier(login, password)

        assert response.status_code == 200
        assert "id" in response.json()

    def test_login_courier_with_wrong_password(self, courier):
        """Система вернёт ошибку, если неправильно указать пароль"""
        login_pass = register_new_courier_and_return_login_password()
        login, password, first_name = login_pass
        courier.append((login, password))

        response = login_courier(login, "wrong_password")

        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"

    def test_login_courier_with_wrong_login(self, courier):
        """Система вернёт ошибку, если неправильно указать логин"""
        login_pass = register_new_courier_and_return_login_password()
        login, password, first_name = login_pass
        courier.append((login, password))

        response = login_courier("wrong_login", password)

        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"

    @pytest.mark.parametrize("field", ["login"])
    def test_login_courier_without_field(self, courier, field):
        """Если какого-то поля нет, запрос возвращает ошибку"""
        login_pass = register_new_courier_and_return_login_password()
        login, password, first_name = login_pass
        courier.append((login, password))

        payload = {"login": login, "password": password}
        payload.pop(field)

        response = requests.post(COURIER_LOGIN_ENDPOINT, data=payload)

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для входа"

    def test_login_nonexistent_courier(self):
        """Если авторизоваться под несуществующим пользователем, запрос возвращает ошибку"""
        response = login_courier("nonexistent_user_123", "nonexistent_pass_123")

        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"