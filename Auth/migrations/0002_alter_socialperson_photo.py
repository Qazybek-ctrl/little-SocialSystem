# Generated by Django 4.0.5 on 2022-06-19 11:22

import Auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialperson',
            name='photo',
            field=models.ImageField(blank=True, default='', upload_to=Auth.models.user_directory_path),
        ),
    ]
