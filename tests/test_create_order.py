import pytest
import requests
import allure

from config import ORDERS_ENDPOINT
from data import ORDER_DATA, COLORS


@allure.feature("Создание заказа")
class TestCreateOrder:
    """Тесты для ручки «Создание заказа»"""

    @pytest.mark.parametrize("color", COLORS)
    def test_create_order_with_colors(self, color):
        """Заказ можно создать с разными вариантами цветов"""
        payload = ORDER_DATA.copy()
        payload["color"] = color

        response = requests.post(ORDERS_ENDPOINT, json=payload)

        assert response.status_code == 201
        assert "track" in response.json()

    def test_create_order_returns_track(self):
        """Тело ответа содержит track"""
        payload = ORDER_DATA.copy()
        payload["color"] = ["BLACK"]

        response = requests.post(ORDERS_ENDPOINT, json=payload)

        assert response.status_code == 201
        assert "track" in response.json()
        assert isinstance(response.json()["track"], int)