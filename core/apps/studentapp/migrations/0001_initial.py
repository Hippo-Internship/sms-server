# Generated by Django 3.2.4 on 2021-08-02 05:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('utilityapp', '0001_initial'),
        ('classapp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schoolapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=56, unique=True)),
                ('percent', models.FloatField(blank=True, null=True)),
                ('value', models.IntegerField(blank=True, null=True)),
                ('limited', models.BooleanField(default=False, null=True)),
                ('limit', models.IntegerField(blank=True, default=0)),
                ('count', models.IntegerField(blank=True, default=0)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discounts', to='schoolapp.branch')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('created', models.DateField(auto_now_add=True)),
                ('modified', models.DateField(auto_now=True)),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('discount_amount', models.FloatField(default=0)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('note', models.CharField(blank=True, max_length=255, null=True)),
                ('canceled', models.BooleanField(default=False)),
                ('_class', models.ForeignKey(db_column='class', on_delete=django.db.models.deletion.CASCADE, related_name='students', to='classapp.class')),
                ('discounts', models.ManyToManyField(blank=True, to='studentapp.Discount')),
                ('operator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registered_students', to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='utilityapp.status')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['id'],
                'unique_together': {('user', '_class')},
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('paid', models.FloatField()),
                ('is_debit', models.BooleanField(default=False)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='schoolapp.branch')),
                ('pay_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='utilityapp.paymentmethod')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='studentapp.student')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('created', models.DateField(auto_now_add=True)),
                ('modified', models.DateField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('body', models.CharField(max_length=255)),
                ('operator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='student_notes', to=settings.AUTH_USER_MODEL)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='studentapp.student')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('state', models.BooleanField(blank=True, default=False, null=True)),
                ('calendar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='journals', to='classapp.calendar')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='journals', to='studentapp.student')),
            ],
        ),
        migrations.CreateModel(
            name='ExamResult',
            fields=[
                ('created', models.DateField(auto_now_add=True)),
                ('modified', models.DateField(auto_now=True)),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('mark', models.IntegerField(default=0)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='classapp.exam')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exam_results', to='studentapp.student')),
            ],
            options={
                'ordering': ['id'],
                'unique_together': {('exam', 'student')},
            },
        ),
    ]
