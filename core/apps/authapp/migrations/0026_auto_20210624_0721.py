# Generated by Django 3.2.4 on 2021-06-24 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0025_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='address_appartment',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='address_city',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='address_district',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='address_khoroo',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='register',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]