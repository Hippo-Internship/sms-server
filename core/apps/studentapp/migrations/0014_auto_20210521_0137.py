# Generated by Django 3.2.2 on 2021-05-21 01:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classapp', '0007_exam'),
        ('studentapp', '0013_examresult_journal'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='examresult',
            options={'ordering': ['id']},
        ),
        migrations.AlterUniqueTogether(
            name='examresult',
            unique_together={('exam', 'student')},
        ),
    ]