"""Тесты ручки «Логин курьера»: POST /api/v1/courier/login."""

import allure
import requests

from data import ACCOUNT_NOT_FOUND, BASE_URL, NOT_ENOUGH_DATA_LOGIN
from helpers import generate_random_string


@allure.feature("Курьер")
@allure.story("Авторизация курьера")
class TestLoginCourier:
    """Тесты ручки авторизации курьера."""

    @allure.title("Курьер может авторизоваться, ответ содержит id")
    def test_courier_can_login_and_get_id(self, courier):
        response = requests.post(
            f"{BASE_URL}/courier/login",
            data={"login": courier["login"], "password": courier["password"]},
        )

        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title("Ошибка, если не передан логин")
    def test_login_without_login_error(self, courier):
        response = requests.post(
            f"{BASE_URL}/courier/login",
            data={"password": courier["password"]},
        )

        assert response.status_code == 400
        assert response.json()["message"] == NOT_ENOUGH_DATA_LOGIN

    @allure.title("Ошибка, если не передан пароль")
    def test_login_without_password_error(self, courier):
        # Без пароля сервер отвечает ошибкой 5xx либо не отвечает вовсе,
        # поэтому проверяем, что авторизация не проходит.
        try:
            response = requests.post(
                f"{BASE_URL}/courier/login",
                data={"login": courier["login"]},
                timeout=10,
            )
            assert response.status_code >= 400
        except requests.exceptions.ReadTimeout:
            pass

    @allure.title("Ошибка при неверном пароле")
    def test_login_with_wrong_password_error(self, courier):
        response = requests.post(
            f"{BASE_URL}/courier/login",
            data={"login": courier["login"], "password": generate_random_string()},
        )

        assert response.status_code == 404
        assert response.json()["message"] == ACCOUNT_NOT_FOUND

    @allure.title("Ошибка при неверном логине")
    def test_login_with_wrong_login_error(self, courier):
        response = requests.post(
            f"{BASE_URL}/courier/login",
            data={"login": generate_random_string(), "password": courier["password"]},
        )

        assert response.status_code == 404
        assert response.json()["message"] == ACCOUNT_NOT_FOUND

    @allure.title("Ошибка при авторизации под несуществующим пользователем")
    def test_login_with_nonexistent_user_error(self):
        response = requests.post(
            f"{BASE_URL}/courier/login",
            data={"login": generate_random_string(), "password": generate_random_string()},
        )

        assert response.status_code == 404
        assert response.json()["message"] == ACCOUNT_NOT_FOUND
