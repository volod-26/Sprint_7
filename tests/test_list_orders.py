import requests
import allure

from config import ORDERS_ENDPOINT


@allure.feature("Список заказов")
class TestListOrders:
    """Тесты для ручки «Список заказов»"""

    def test_get_list_orders(self):
        """В тело ответа возвращается список заказов"""
        response = requests.get(ORDERS_ENDPOINT)

        assert response.status_code == 200
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)