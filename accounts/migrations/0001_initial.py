# Generated by Django 3.2.4 on 2021-11-03 05:09

import address.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('address', '0004_auto_20211103_1039'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Retailer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_name', models.CharField(max_length=100)),
                ('sale_tax_number', models.CharField(max_length=20)),
                ('contact_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('address', address.models.AddressField(on_delete=django.db.models.deletion.CASCADE, to='address.address')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
