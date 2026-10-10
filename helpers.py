import random
import string
import requests

from config import COURIER_ENDPOINT, COURIER_LOGIN_ENDPOINT


def generate_random_string(length):
    """Генерирует случайную строку из букв нижнего регистра"""
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string


def register_new_courier_and_return_login_password():
    """Регистрирует нового курьера и возвращает [login, password, firstName]"""
    login_pass = []
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(COURIER_ENDPOINT, data=payload)

    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    return login_pass


def delete_courier(login, password):
    """Удаляет курьера по логину и паролю"""
    login_response = requests.post(
        COURIER_LOGIN_ENDPOINT,
        data={"login": login, "password": password}
    )
    if login_response.status_code == 200:
        courier_id = login_response.json()["id"]
        requests.delete(f"{COURIER_ENDPOINT}/{courier_id}")