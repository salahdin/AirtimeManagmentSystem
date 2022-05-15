from django.conf import settings
import requests


topup_message = """
Dear Customer your have received an airtime topup from your organization
"""


def send_sms(phone, amount, organization, name):
    details = settings.SMS_API
    url = details['server'] + "/services/send.php"
    message = f'Dear {name} you have received an airtime topup of {amount} Birr from {organization}'
    args = {
        'key': details['api_key'],
        'number': phone,
        'message': message,
        'device': '5178',
    }
    r = requests.get(url=url, params=args)
