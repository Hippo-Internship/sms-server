# Generated by Django 3.2 on 2021-05-10 06:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classapp', '0002_auto_20210507_0556'),
    ]

    operations = [
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('day', models.IntegerField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')])),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('_class', models.ForeignKey(db_column='class', on_delete=django.db.models.deletion.CASCADE, related_name='dates', to='classapp.class')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
