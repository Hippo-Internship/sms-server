# Generated by Django 3.2.4 on 2021-06-26 05:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schoolapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=56)),
                ('start_date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_date', models.DateField()),
                ('end_time', models.TimeField()),
                ('note', models.CharField(blank=True, max_length=255, null=True)),
                ('interval', models.PositiveIntegerField(blank=True, null=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classes', to='schoolapp.branch')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('created', models.DateField(auto_now_add=True)),
                ('modified', models.DateField(auto_now=True)),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(db_index=True, error_messages={'unique': 'Name is already registered!'}, max_length=50, unique=True)),
                ('capacity', models.PositiveIntegerField(default=0)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='schoolapp.branch')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('created', models.DateField(auto_now_add=True)),
                ('modified', models.DateField(auto_now=True)),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(db_index=True, error_messages={'unique': 'Name is already regeistered!'}, max_length=50, unique=True)),
                ('short_name', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('interval', models.PositiveIntegerField(default=0, null=True)),
                ('is_online_pay', models.BooleanField(blank=True, null=True)),
                ('price', models.PositiveIntegerField()),
                ('color', models.CharField(default='#3d3f56', max_length=50)),
                ('sort', models.PositiveIntegerField(blank=True, null=True)),
                ('exam', models.PositiveIntegerField(default=0, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='schoolapp.branch')),
            ],
            options={
                'ordering': ['id'],
                'unique_together': {('branch', 'name')},
            },
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=24)),
                ('total_mark', models.IntegerField(default=0)),
                ('date', models.DateField()),
                ('_class', models.ForeignKey(db_column='class', on_delete=django.db.models.deletion.CASCADE, related_name='exams', to='classapp.class')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='class',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='classes', to='classapp.lesson'),
        ),
        migrations.AddField(
            model_name='class',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='classes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('_class', models.ForeignKey(db_column='class', on_delete=django.db.models.deletion.CASCADE, related_name='calendar', to='classapp.class')),
                ('room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='calendar', to='classapp.room')),
            ],
            options={
                'ordering': ['id'],
                'unique_together': {('room', 'date', 'start_time')},
            },
        ),
    ]
