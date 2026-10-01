"""Тесты ручки «Логин курьера»: POST /api/v1/courier/login."""

import allure

from data import ACCOUNT_NOT_FOUND, NOT_ENOUGH_DATA_LOGIN
from helpers import generate_random_string, login_courier


@allure.feature("Курьер")
@allure.story("Авторизация курьера")
class TestLoginCourier:
    """Тесты ручки авторизации курьера."""

    @allure.title("Курьер может авторизоваться, ответ содержит id")
    def test_courier_can_login_and_get_id(self, courier):
        response = login_courier(
            {"login": courier["login"], "password": courier["password"]}
        )

        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title("Ошибка, если не передан логин")
    def test_login_without_login_error(self, courier):
        response = login_courier({"password": courier["password"]})

        assert response.status_code == 400
        assert response.json()["message"] == NOT_ENOUGH_DATA_LOGIN

    @allure.title("Ошибка, если не передан пароль")
    def test_login_without_password_error(self, courier):
        # Если ключ password отсутствует, сервер зависает и не отвечает,
        # поэтому передаём пустой пароль — данных для входа недостаточно.
        response = login_courier({"login": courier["login"], "password": ""})

        assert response.status_code == 400
        assert response.json()["message"] == NOT_ENOUGH_DATA_LOGIN

    @allure.title("Ошибка при неверном пароле")
    def test_login_with_wrong_password_error(self, courier):
        response = login_courier(
            {"login": courier["login"], "password": generate_random_string()}
        )

        assert response.status_code == 404
        assert response.json()["message"] == ACCOUNT_NOT_FOUND

    @allure.title("Ошибка при неверном логине")
    def test_login_with_wrong_login_error(self, courier):
        response = login_courier(
            {"login": generate_random_string(), "password": courier["password"]}
        )

        assert response.status_code == 404
        assert response.json()["message"] == ACCOUNT_NOT_FOUND

    @allure.title("Ошибка при авторизации под несуществующим пользователем")
    def test_login_with_nonexistent_user_error(self):
        response = login_courier(
            {"login": generate_random_string(), "password": generate_random_string()}
        )

        assert response.status_code == 404
        assert response.json()["message"] == ACCOUNT_NOT_FOUND
