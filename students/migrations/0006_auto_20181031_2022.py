# Generated by Django 2.0.6 on 2018-10-31 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0005_auto_20181024_1631'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='file',
        ),
        migrations.AddField(
            model_name='project',
            name='filename',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
