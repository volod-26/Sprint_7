import pytest
import requests
import helpers

from config import COURIER_ENDPOINT, COURIER_LOGIN_ENDPOINT, ORDERS_ENDPOINT


@pytest.fixture
def courier():
    """Фикстура: создаёт курьера и удаляет после теста"""
    login_pass = helpers.register_new_courier_and_return_login_password()
    yield login_pass
    if login_pass:
        helpers.delete_courier(login_pass[0], login_pass[1])


@pytest.fixture
def courier_with_cleanup():
    """Фикстура: создаёт курьера, удаляет после теста (даже если тест упал)"""
    login_pass = helpers.register_new_courier_and_return_login_password()
    yield login_pass
    if login_pass:
        helpers.delete_courier(login_pass[0], login_pass[1])