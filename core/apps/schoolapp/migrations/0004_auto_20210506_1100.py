# Generated by Django 3.2 on 2021-05-06 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolapp', '0003_auto_20210506_0218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='name',
            field=models.CharField(error_messages={'unique': 'Name is already registered!'}, max_length=36, unique=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='name',
            field=models.CharField(error_messages={'unique': 'Name is already registered!'}, max_length=36, unique=True),
        ),
    ]
