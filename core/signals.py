from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal

from core.models import Config

@receiver(post_save, sender=Config)
def update_config_handler(sender, instance, created, **kwargs):
    # Update your settings value here
    Updated_SMS_API = {
        'server': instance.server,
        'api_key': instance.api_key,
    }
    settings.SMS_API = Updated_SMS_API
