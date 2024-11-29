import requests
from .models import Devise
from django.conf import from django.conf import settings


EXCHANGE_API_URL = ''

def fetch_exchange_rate():
    response = request.get(EXCHANGE_API_URL)
    if response.status_code == 200:
        data = response.json()

        if data['result'] == 'success':
            rate = data['conversion_rates'].get('RUB')
            if rate:
                exchange_rate, created = Devise.objects.update_or_create(
                    base_currency='XAF',
                    target_currency='RUB',
                    default={'rate':rate}
                )

                return rate
        return None