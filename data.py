"""Данные и адрес для тестов API Яндекс Самокат."""

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"

# Тексты ошибок, которые возвращает сервер.
COURIER_ALREADY_EXISTS = "Этот логин уже используется. Попробуйте другой."
NOT_ENOUGH_DATA_CREATE = "Недостаточно данных для создания учетной записи"
NOT_ENOUGH_DATA_LOGIN = "Недостаточно данных для входа"
ACCOUNT_NOT_FOUND = "Учетная запись не найдена"

# Шаблон заказа для тестов.
ORDER = {
    "firstName": "Naruto",
    "lastName": "Uchiha",
    "address": "Konoha, 142 apt.",
    "metroStation": "4",
    "phone": "+7 800 355 35 35",
    "rentTime": 5,
    "deliveryDate": "2020-06-06",
    "comment": "Saske, come back to Konoha",
}

# Варианты цветов для проверки создания заказа.
ORDER_COLORS = [
    ["BLACK"],
    ["GREY"],
    ["BLACK", "GREY"],
    [],
]
