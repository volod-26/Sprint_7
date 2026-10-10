import pytest
import requests
import helpers
import allure

from config import COURIER_LOGIN_ENDPOINT


@allure.feature("Логин курьера")
class TestLoginCourier:
    """Тесты для ручки «Логин курьера»"""

    @allure.step("Авторизовать курьера")
    def login_courier(self, login, password):
        return requests.post(
            COURIER_LOGIN_ENDPOINT,
            data={"login": login, "password": password}
        )

    def test_login_courier_success(self, courier):
        """Курьер может авторизоваться"""
        login, password, first_name = courier

        response = self.login_courier(login, password)

        assert response.status_code == 200
        assert "id" in response.json()

    def test_login_courier_with_wrong_password(self, courier):
        """Система вернёт ошибку, если неправильно указать пароль"""
        login, password, first_name = courier

        response = self.login_courier(login, "wrong_password")

        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"

    def test_login_courier_with_wrong_login(self, courier):
        """Система вернёт ошибку, если неправильно указать логин"""
        login, password, first_name = courier

        response = self.login_courier("wrong_login", password)

        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"

    @pytest.mark.parametrize("field", ["login"])
    def test_login_courier_without_field(self, courier, field):
        """Если какого-то поля нет, запрос возвращает ошибку"""
        login, password, first_name = courier
        payload = {"login": login, "password": password}
        payload.pop(field)

        response = requests.post(COURIER_LOGIN_ENDPOINT, data=payload)

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для входа"

    def test_login_nonexistent_courier(self):
        """Если авторизоваться под несуществующим пользователем, запрос возвращает ошибку"""
        response = self.login_courier("nonexistent_user_123", "nonexistent_pass_123")

        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"