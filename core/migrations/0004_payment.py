# Generated by Django 4.0.1 on 2022-04-06 05:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_wallet_company'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('date', models.DateTimeField()),
                ('payment_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company', to='core.company')),
                ('payment_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee', to='core.employee')),
            ],
        ),
    ]
