# Generated by Django 3.2 on 2021-05-06 03:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('authapp', '0012_auto_20210506_0319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='groups',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='auth.group'),
            preserve_default=False,
        ),
    ]