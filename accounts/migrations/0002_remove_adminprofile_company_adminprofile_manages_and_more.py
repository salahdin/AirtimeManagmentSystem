# Generated by Django 4.0.1 on 2022-04-07 07:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0004_payment'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adminprofile',
            name='company',
        ),
        migrations.AddField(
            model_name='adminprofile',
            name='manages',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='manager', to='core.company'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='adminprofile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]