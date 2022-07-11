from django.conf import settings
from .models import Config
import requests


def send_sms(phone, amount, organization, name):
    details = Config.objects.first()
    url = details.server + "/services/send.php"
    message = f'Dear {name} you have received an airtime topup of {amount} Birr from {organization}'
    args = {
        'key': details.api_key,
        'number': phone,
        'message': message,
        'device': details.device,
        'sim': details.sim
    }
    r = requests.get(url=url, params=args)
