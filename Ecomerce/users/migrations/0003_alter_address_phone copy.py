# Generated by Django 4.2.7 on 2023-12-20 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_address_phone_number_address_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='phone',
            field=models.CharField(default='', max_length=15),
        ),
    ]
