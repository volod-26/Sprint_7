import pytest
import requests
import helpers


BASE_URL = "https://qa-scooter.praktikum-services.ru"


class TestLoginCourier:
    """Тесты для ручки «Логин курьера»"""

    def test_login_courier_success(self):
        """Курьер может авторизоваться"""
        login_pass = helpers.register_new_courier_and_return_login_password()
        login, password, first_name = login_pass

        response = requests.post(
            f"{BASE_URL}/api/v1/courier/login",
            data={"login": login, "password": password}
        )

        assert response.status_code == 200
        assert "id" in response.json()

        # Удаляем курьера
        courier_id = response.json()["id"]
        requests.delete(f"{BASE_URL}/api/v1/courier/{courier_id}")

    def test_login_courier_with_wrong_password(self):
        """Система вернёт ошибку, если неправильно указать пароль"""
        login_pass = helpers.register_new_courier_and_return_login_password()
        login, password, first_name = login_pass

        response = requests.post(
            f"{BASE_URL}/api/v1/courier/login",
            data={"login": login, "password": "wrong_password"}
        )

        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"

        # Удаляем курьера
        login_response = requests.post(
            f"{BASE_URL}/api/v1/courier/login",
            data={"login": login, "password": password}
        )
        courier_id = login_response.json()["id"]
        requests.delete(f"{BASE_URL}/api/v1/courier/{courier_id}")

    def test_login_courier_with_wrong_login(self):
        """Система вернёт ошибку, если неправильно указать логин"""
        login_pass = helpers.register_new_courier_and_return_login_password()
        login, password, first_name = login_pass

        response = requests.post(
            f"{BASE_URL}/api/v1/courier/login",
            data={"login": "wrong_login", "password": password}
        )

        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"

        # Удаляем курьера
        login_response = requests.post(
            f"{BASE_URL}/api/v1/courier/login",
            data={"login": login, "password": password}
        )
        courier_id = login_response.json()["id"]
        requests.delete(f"{BASE_URL}/api/v1/courier/{courier_id}")

    @pytest.mark.parametrize("field", ["login"])
    def test_login_courier_without_field(self, field):
        """Если какого-то поля нет, запрос возвращает ошибку"""
        login_pass = helpers.register_new_courier_and_return_login_password()
        login, password, first_name = login_pass

        payload = {"login": login, "password": password}
        payload.pop(field)

        response = requests.post(f"{BASE_URL}/api/v1/courier/login", data=payload)

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для входа"

        # Удаляем курьера
        login_response = requests.post(
            f"{BASE_URL}/api/v1/courier/login",
            data={"login": login, "password": password}
        )
        courier_id = login_response.json()["id"]
        requests.delete(f"{BASE_URL}/api/v1/courier/{courier_id}")

    def test_login_nonexistent_courier(self):
        """Если авторизоваться под несуществующим пользователем, запрос возвращает ошибку"""
        response = requests.post(
            f"{BASE_URL}/api/v1/courier/login",
            data={"login": "nonexistent_user_123", "password": "nonexistent_pass_123"}
        )

        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"