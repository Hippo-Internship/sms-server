# Generated by Django 3.2.2 on 2021-05-21 01:59

import core.functions
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0024_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=core.functions.PathAndRename('image/profiles')),
        ),
    ]