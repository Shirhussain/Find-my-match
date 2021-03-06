# Generated by Django 3.1.5 on 2021-01-22 15:01

from django.db import migrations, models
import profiles.models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_userjob'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.ImageField(blank=True, default='avatar.jpeg', null=True, upload_to=profiles.models.upload_location, verbose_name='Picture'),
        ),
    ]
