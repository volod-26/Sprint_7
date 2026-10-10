import pytest
import requests
import helpers
import allure

from config import COURIER_ENDPOINT


@allure.feature("Создание курьера")
class TestCreateCourier:
    """Тесты для ручки «Создание курьера»"""

    @allure.step("Создать курьера")
    def create_courier(self, login, password, first_name):
        return requests.post(
            COURIER_ENDPOINT,
            data={"login": login, "password": password, "firstName": first_name}
        )

    def test_create_courier_success(self, courier_with_cleanup):
        """Курьера можно создать"""
        login, password, first_name = courier_with_cleanup

        response = self.create_courier(
            helpers.generate_random_string(10),
            helpers.generate_random_string(10),
            helpers.generate_random_string(10)
        )

        assert response.status_code == 201
        assert response.json() == {"ok": True}

    def test_create_two_identical_couriers(self, courier):
        """Нельзя создать двух одинаковых курьеров"""
        login, password, first_name = courier

        response = self.create_courier(login, password, first_name)

        assert response.status_code == 409
        assert response.json()["message"] == "Этот логин уже используется. Попробуйте другой."

    @pytest.mark.parametrize("field", ["login", "password"])
    def test_create_courier_without_field(self, field):
        """Чтобы создать курьера, нужно передать все обязательные поля"""
        payload = {
            "login": helpers.generate_random_string(10),
            "password": helpers.generate_random_string(10),
            "firstName": helpers.generate_random_string(10)
        }
        payload.pop(field)

        response = requests.post(COURIER_ENDPOINT, data=payload)

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"