# Generated by Django 3.2.2 on 2021-06-10 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentapp', '0015_journal_calendar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]