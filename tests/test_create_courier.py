"""Тесты ручки «Создать курьера»: POST /api/v1/courier."""

import allure
import pytest
import requests

from data import BASE_URL, COURIER_ALREADY_EXISTS, NOT_ENOUGH_DATA_CREATE
from helpers import generate_random_string


@allure.feature("Курьер")
@allure.story("Создание курьера")
class TestCreateCourier:
    """Тесты ручки создания курьера."""

    @allure.title("Курьера можно создать")
    def test_create_courier_success(self, courier_data):
        response = requests.post(f"{BASE_URL}/courier", data=courier_data)

        assert response.status_code == 201
        assert response.json() == {"ok": True}

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_two_identical_couriers_error(self, courier_data):
        requests.post(f"{BASE_URL}/courier", data=courier_data)
        response = requests.post(f"{BASE_URL}/courier", data=courier_data)

        assert response.status_code == 409
        assert response.json()["message"] == COURIER_ALREADY_EXISTS

    @allure.title("Ошибка при создании курьера с занятым логином")
    def test_create_courier_with_existing_login_error(self, courier):
        payload = {
            "login": courier["login"],
            "password": generate_random_string(),
            "firstName": generate_random_string(),
        }

        response = requests.post(f"{BASE_URL}/courier", data=payload)

        assert response.status_code == 409
        assert response.json()["message"] == COURIER_ALREADY_EXISTS

    @allure.title("Ошибка, если не передано обязательное поле")
    @pytest.mark.parametrize("field", ["login", "password"])
    def test_create_courier_without_required_field_error(self, field):
        payload = {
            "login": generate_random_string(),
            "password": generate_random_string(),
            "firstName": generate_random_string(),
        }
        payload.pop(field)

        response = requests.post(f"{BASE_URL}/courier", data=payload)

        assert response.status_code == 400
        assert response.json()["message"] == NOT_ENOUGH_DATA_CREATE

    @allure.title("Ошибка при создании курьера без данных")
    def test_create_courier_without_fields_error(self):
        response = requests.post(f"{BASE_URL}/courier", data={})

        assert response.status_code == 400
        assert response.json()["message"] == NOT_ENOUGH_DATA_CREATE
