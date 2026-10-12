import pytest
import requests
import helpers

from config import COURIER_ENDPOINT, COURIER_LOGIN_ENDPOINT


@pytest.fixture
def courier():
    """Фикстура: пустой список для курьеров, удаление после теста"""
    created_couriers = []
    yield created_couriers
    # Постусловие: удаляем всех созданных курьеров
    for login, password in created_couriers:
        helpers.delete_courier(login, password)