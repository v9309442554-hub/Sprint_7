"""Тесты ручки «Создать заказ»: POST /api/v1/orders."""

import allure
import pytest

from data import ORDER, ORDER_COLORS
from helpers import create_order


@allure.feature("Заказ")
@allure.story("Создание заказа")
class TestCreateOrder:
    """Тесты ручки создания заказа."""

    @allure.title("Заказ можно создать с одним цветом, с двумя или без цвета")
    @pytest.mark.parametrize(
        "color", ORDER_COLORS, ids=["BLACK", "GREY", "BLACK и GREY", "без цвета"]
    )
    def test_create_order_with_color(self, color):
        order = dict(ORDER)
        order["color"] = color

        response = create_order(order)

        assert response.status_code == 201
        assert "track" in response.json()

    @allure.title("Заказ можно создать без поля color")
    def test_create_order_without_color(self):
        response = create_order(ORDER)

        assert response.status_code == 201
        assert "track" in response.json()
