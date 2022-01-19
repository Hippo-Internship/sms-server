# Generated by Django 3.2.4 on 2021-08-03 06:19

import core.apps.authapp.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('schoolapp', '0001_initial'),
        # ('auth', '0013_group_role_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('firstname', models.CharField(max_length=56)),
                ('lastname', models.CharField(blank=True, max_length=56, null=True)),
                ('username', models.CharField(blank=True, max_length=56, null=True)),
                ('email', models.EmailField(blank=True, error_messages={'unique': 'This email is already registered!'}, max_length=254, null=True, unique=True)),
                ('password', models.CharField(blank=True, max_length=128, null=True, verbose_name='password')),
                ('phone', models.CharField(max_length=20, validators=[core.apps.authapp.validators.validate_phone])),
                ('related_phone', models.CharField(blank=True, max_length=20, null=True, validators=[core.apps.authapp.validators.validate_phone])),
                ('interested_at', models.CharField(blank=True, max_length=255, null=True)),
                ('seen_datasheet', models.IntegerField(blank=True, choices=[(1, 'Created from datasheet'), (2, 'Student and registered in datasheet'), (3, 'Created from student')], default=3)),
                ('is_active', models.BooleanField(default=True)),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='schoolapp.branch')),
                ('groups', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='auth.group')),
                ('school', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='schoolapp.school')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to='image/profiles')),
                ('address_city', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('address_district', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('address_khoroo', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('address_apartment', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('dob', models.DateField(blank=True, max_length=255, null=True)),
                ('register', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]