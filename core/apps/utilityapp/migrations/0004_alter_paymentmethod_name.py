# Generated by Django 3.2.4 on 2021-07-06 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utilityapp', '0003_auto_20210706_0015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentmethod',
            name='name',
            field=models.CharField(max_length=26),
        ),
    ]
