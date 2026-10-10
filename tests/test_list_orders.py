import requests
import allure

from config import ORDERS_ENDPOINT


@allure.feature("Список заказов")
class TestListOrders:
    """Тесты для ручки «Список заказов»"""

    @allure.step("Получить список заказов")
    def get_orders(self):
        return requests.get(ORDERS_ENDPOINT)

    def test_get_list_orders(self):
        """В тело ответа возвращается список заказов"""
        response = self.get_orders()

        assert response.status_code == 200
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)