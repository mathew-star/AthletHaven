# Generated by Django 4.2.7 on 2023-12-14 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0002_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(upload_to='category/'),
        ),
    ]
