# Generated by Django 3.1.5 on 2021-01-09 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0006_auto_20210109_0922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useranswer',
            name='their_points',
            field=models.IntegerField(blank=True, default=-1, null=True, verbose_name='My points'),
        ),
    ]
