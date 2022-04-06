from django.contrib.auth.models import User
from django.db import models
from core.models import Company


class AdminProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ManyToManyField(Company, blank=True)
    img = models.ImageField(upload_to='core/avatar', blank=True, default='core/avatar/blank_profile.png')

    def __str__(self):
        return (str(self.user))