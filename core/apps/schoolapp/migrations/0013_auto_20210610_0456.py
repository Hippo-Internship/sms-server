# Generated by Django 3.2.2 on 2021-06-10 04:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schoolapp', '0012_alter_school_logo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='branch',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='school',
            options={'ordering': ['-id']},
        ),
    ]