# Generated by Django 3.2 on 2021-05-05 06:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0007_auto_20210505_0602'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='role_id',
        ),
    ]
