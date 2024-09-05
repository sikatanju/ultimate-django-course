from django.contrib.auth.models import User

from rest_framework.test import APIClient

import pytest

#* To make this a fixuture, just use the decorator

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticate(api_client):
    # def do_authenticate(user): #* My implementation
    #     return api_client.force_authenticate(user=user)
    def do_authenticate(is_staff=False):
        return api_client.force_authenticate(user=User(is_staff=is_staff))
    
    return do_authenticate