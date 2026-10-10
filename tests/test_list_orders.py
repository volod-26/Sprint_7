import requests


BASE_URL = "https://qa-scooter.praktikum-services.ru"


class TestListOrders:
    """Тесты для ручки «Список заказов»"""

    def test_get_list_orders(self):
        """В тело ответа возвращается список заказов"""
        response = requests.get(f"{BASE_URL}/api/v1/orders")

        assert response.status_code == 200
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)