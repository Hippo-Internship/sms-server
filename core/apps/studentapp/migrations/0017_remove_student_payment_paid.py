# Generated by Django 3.2.4 on 2021-06-14 06:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studentapp', '0016_auto_20210610_0456'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='payment_paid',
        ),
    ]
