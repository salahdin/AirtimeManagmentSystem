# Generated by Django 4.0.1 on 2022-04-16 11:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_from',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='core.company'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='core.employee'),
        ),
    ]