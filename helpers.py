"""Вспомогательные функции: генерация данных и шаги (запросы) для Allure."""

import random
import string

import allure
import requests

from data import BASE_URL


def generate_random_string(length=10):
    """Возвращает случайную строку из букв нижнего регистра."""
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


@allure.step("Создать курьера: POST /courier")
def create_courier(payload):
    """Отправляет запрос на создание курьера."""
    return requests.post(f"{BASE_URL}/courier", data=payload)


@allure.step("Авторизовать курьера: POST /courier/login")
def login_courier(payload):
    """Отправляет запрос на авторизацию курьера."""
    return requests.post(f"{BASE_URL}/courier/login", data=payload)


@allure.step("Удалить курьера: DELETE /courier/{courier_id}")
def delete_courier(courier_id):
    """Удаляет курьера по его id."""
    return requests.delete(f"{BASE_URL}/courier/{courier_id}")


@allure.step("Удалить курьера по логину и паролю")
def delete_courier_by_login_password(login, password):
    """Удаляет курьера: сначала получает id, затем удаляет."""
    response = login_courier({"login": login, "password": password})
    if response.status_code == 200:
        delete_courier(response.json()["id"])


@allure.step("Создать заказ: POST /orders")
def create_order(order):
    """Отправляет запрос на создание заказа."""
    return requests.post(f"{BASE_URL}/orders", json=order)


@allure.step("Получить список заказов: GET /orders")
def get_orders():
    """Запрашивает список заказов."""
    return requests.get(f"{BASE_URL}/orders")


def register_new_courier_and_return_login_password():
    """Регистрирует нового курьера и возвращает [логин, пароль, имя].

    Если регистрация не удалась, возвращает пустой список.
    """
    login = generate_random_string()
    password = generate_random_string()
    first_name = generate_random_string()

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name,
    }

    response = create_courier(payload)

    if response.status_code == 201:
        return [login, password, first_name]
    return []
