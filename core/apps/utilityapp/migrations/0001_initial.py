# Generated by Django 3.2 on 2021-05-10 08:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('schoolapp', '0004_auto_20210506_1100'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('created', models.DateField(auto_now_add=True)),
                ('modified', models.DateField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=26, unique=True)),
                ('color', models.CharField(default='#3d3f56', max_length=7)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schoolapp.branch')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]