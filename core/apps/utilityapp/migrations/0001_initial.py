# Generated by Django 3.2.4 on 2021-08-03 06:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('schoolapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('created', models.DateField(auto_now_add=True)),
                ('modified', models.DateField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=26)),
                ('color', models.CharField(default='#3d3f56', max_length=7)),
                ('default', models.BooleanField(default=False)),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='status', to='schoolapp.branch')),
            ],
            options={
                'ordering': ['-default', '-id'],
                'unique_together': {('branch', 'name')},
            },
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('created', models.DateField(auto_now_add=True)),
                ('modified', models.DateField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=26)),
                ('default', models.BooleanField(default=False)),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment_method', to='schoolapp.branch')),
            ],
            options={
                'ordering': ['-default', '-id'],
                'unique_together': {('branch', 'name')},
            },
        ),
    ]
