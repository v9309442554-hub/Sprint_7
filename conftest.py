"""Фикстуры: подготовка тестовых данных и удаление их после теста."""

import pytest

from helpers import (
    delete_courier_by_login_password,
    generate_random_string,
    register_new_courier_and_return_login_password,
)


@pytest.fixture
def courier_data():
    """Данные нового курьера. Созданный в тесте курьер удаляется после теста."""
    payload = {
        "login": generate_random_string(),
        "password": generate_random_string(),
        "firstName": generate_random_string(),
    }

    yield payload

    delete_courier_by_login_password(payload["login"], payload["password"])


@pytest.fixture
def courier():
    """Создаёт курьера перед тестом и удаляет его после теста."""
    login, password, first_name = register_new_courier_and_return_login_password()

    yield {"login": login, "password": password, "firstName": first_name}

    delete_courier_by_login_password(login, password)
