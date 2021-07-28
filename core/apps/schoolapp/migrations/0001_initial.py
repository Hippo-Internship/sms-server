# Generated by Django 3.2.4 on 2021-07-27 07:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('created', models.DateField(auto_now_add=True)),
                ('modified', models.DateField(auto_now=True)),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(error_messages={'unique': 'Name is already registered!'}, max_length=36, unique=True)),
                ('description', models.CharField(blank=True, max_length=128, null=True)),
                ('address', models.CharField(blank=True, max_length=128, null=True)),
                ('website', models.CharField(blank=True, max_length=52, null=True)),
                ('color', models.CharField(blank=True, default='#3d3f56', max_length=52)),
                ('image', models.ImageField(blank=True, default='image/schools/default-min.jpg', upload_to='image/schools')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='image/schools-logo')),
                ('yearly_goal', models.IntegerField(blank=True, default=0, null=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('created', models.DateField(auto_now_add=True)),
                ('modified', models.DateField(auto_now=True)),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(db_index=True, max_length=36)),
                ('description', models.CharField(blank=True, max_length=128, null=True)),
                ('address', models.CharField(blank=True, max_length=128, null=True)),
                ('website', models.CharField(blank=True, max_length=52, null=True)),
                ('color', models.CharField(default='#3d3f56', max_length=52)),
                ('image', models.ImageField(blank=True, default='image/branches/default_min.jpg', upload_to='image/branches')),
                ('yearly_goal', models.IntegerField(blank=True, default=0, null=True)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branches', to='schoolapp.school')),
            ],
            options={
                'ordering': ['-id'],
                'unique_together': {('school', 'name')},
            },
        ),
    ]
