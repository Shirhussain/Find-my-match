# Generated by Django 3.1.5 on 2021-01-21 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0004_auto_20210121_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employermatch',
            name='liked',
            field=models.BooleanField(null=True, verbose_name='Liked'),
        ),
        migrations.AlterField(
            model_name='jobmatch',
            name='liked',
            field=models.BooleanField(null=True, verbose_name='Liked'),
        ),
        migrations.AlterField(
            model_name='locationmatch',
            name='liked',
            field=models.BooleanField(null=True, verbose_name='Liked'),
        ),
    ]