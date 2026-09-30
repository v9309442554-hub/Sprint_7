"""Простые вспомогательные функции для тестов."""

import random
import string

import requests

from data import BASE_URL


def generate_random_string(length=10):
    """Возвращает случайную строку из букв нижнего регистра."""
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


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

    response = requests.post(f"{BASE_URL}/courier", data=payload)

    login_pass = []
    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    return login_pass


def delete_courier(login, password):
    """Удаляет курьера по логину и паролю, чтобы не оставлять данные."""
    response = requests.post(
        f"{BASE_URL}/courier/login", data={"login": login, "password": password}
    )
    if response.status_code == 200:
        courier_id = response.json()["id"]
        requests.delete(f"{BASE_URL}/courier/{courier_id}")
