# Generated by Django 2.0.6 on 2018-10-31 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0009_auto_20181031_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='filename',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]
