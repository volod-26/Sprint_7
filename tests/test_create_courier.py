import pytest
import requests
import helpers


BASE_URL = "https://qa-scooter.praktikum-services.ru"


class TestCreateCourier:
    """Тесты для ручки «Создание курьера»"""

    def test_create_courier_success(self):
        """Курьера можно создать"""
        login = helpers.generate_random_string(10)
        password = helpers.generate_random_string(10)
        first_name = helpers.generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        response = requests.post(f"{BASE_URL}/api/v1/courier", data=payload)

        assert response.status_code == 201
        assert response.json() == {"ok": True}

        # Удаляем курьера после теста
        login_response = requests.post(
            f"{BASE_URL}/api/v1/courier/login",
            data={"login": login, "password": password}
        )
        courier_id = login_response.json()["id"]
        requests.delete(f"{BASE_URL}/api/v1/courier/{courier_id}")

    def test_create_two_identical_couriers(self):
        """Нельзя создать двух одинаковых курьеров"""
        login_pass = helpers.register_new_courier_and_return_login_password()
        login, password, first_name = login_pass

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        response = requests.post(f"{BASE_URL}/api/v1/courier", data=payload)

        assert response.status_code == 409
        assert response.json()["message"] == "Этот логин уже используется. Попробуйте другой."

        # Удаляем курьера
        login_response = requests.post(
            f"{BASE_URL}/api/v1/courier/login",
            data={"login": login, "password": password}
        )
        courier_id = login_response.json()["id"]
        requests.delete(f"{BASE_URL}/api/v1/courier/{courier_id}")

    @pytest.mark.parametrize("field", ["login", "password"])
    def test_create_courier_without_field(self, field):
        """Чтобы создать курьера, нужно передать все обязательные поля"""
        payload = {
            "login": helpers.generate_random_string(10),
            "password": helpers.generate_random_string(10),
            "firstName": helpers.generate_random_string(10)
        }
        payload.pop(field)

        response = requests.post(f"{BASE_URL}/api/v1/courier", data=payload)

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"