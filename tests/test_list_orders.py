"""Тесты ручки «Список заказов»: GET /api/v1/orders."""

import allure
import requests

from data import BASE_URL


@allure.feature("Заказ")
@allure.story("Список заказов")
class TestListOrders:
    """Тесты ручки получения списка заказов."""

    @allure.title("В ответе возвращается список заказов")
    def test_get_orders_returns_list(self):
        response = requests.get(f"{BASE_URL}/orders")

        assert response.status_code == 200
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)
