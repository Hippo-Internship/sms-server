# Generated by Django 3.2 on 2021-05-10 07:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classapp', '0005_auto_20210510_0727'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='calendar',
            unique_together={('room', 'date', 'start_time')},
        ),
    ]
