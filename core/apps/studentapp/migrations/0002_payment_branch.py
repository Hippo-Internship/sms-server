# Generated by Django 3.2.4 on 2021-06-27 06:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schoolapp', '0001_initial'),
        ('studentapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='branch',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='schoolapp.branch'),
            preserve_default=False,
        ),
    ]
