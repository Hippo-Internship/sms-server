# Generated by Django 3.2.2 on 2021-05-21 01:37

import core.apps.authapp.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0023_auto_20210514_0339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=core.apps.authapp.utils.path_and_rename),
        ),
    ]
