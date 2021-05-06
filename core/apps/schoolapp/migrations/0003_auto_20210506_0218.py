# Generated by Django 3.2 on 2021-05-06 02:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schoolapp', '0002_auto_20210505_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='name',
            field=models.CharField(max_length=36, unique=True),
        ),
        migrations.AlterField(
            model_name='branch',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branches', to='schoolapp.school'),
        ),
    ]
