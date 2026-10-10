import pytest
import requests
import helpers


BASE_URL = "https://qa-scooter.praktikum-services.ru"


class TestCreateOrder:
    """Тесты для ручки «Создание заказа»"""

    @pytest.mark.parametrize("color", [["BLACK"], ["GREY"], ["BLACK", "GREY"], []])
    def test_create_order_with_colors(self, color):
        """Заказ можно создать с разными вариантами цветов"""
        # Создаём заказ
        payload = {
            "firstName": "Иван",
            "lastName": "Иванов",
            "address": "Москва, ул. Ленина, 1",
            "metroStation": 4,
            "phone": "+79991112233",
            "rentTime": 5,
            "deliveryDate": "2026-10-15",
            "comment": "Позвоните за час",
            "color": color
        }

        response = requests.post(f"{BASE_URL}/api/v1/orders", json=payload)

        assert response.status_code == 201
        assert "track" in response.json()

    def test_create_order_returns_track(self):
        """Тело ответа содержит track"""
        payload = {
            "firstName": "Пётр",
            "lastName": "Петров",
            "address": "Москва, ул. Пушкина, 10",
            "metroStation": 5,
            "phone": "+79994445566",
            "rentTime": 3,
            "deliveryDate": "2026-10-16",
            "comment": "Оставьте у подъезда",
            "color": ["BLACK"]
        }

        response = requests.post(f"{BASE_URL}/api/v1/orders", json=payload)

        assert response.status_code == 201
        assert "track" in response.json()
        assert isinstance(response.json()["track"], int)