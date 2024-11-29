import pytest 
from accounts.models import CustomUser
from rest_framework.test import APIClient


@pytest.fixture
def api_client() -> APIClient:
    yield APIClient()


@pytest.fixture
def user() -> CustomUser:
    return CustomUser   .objects.create_user(email='paulnicolas519@gmail.com', password=' ', otp='2345')


