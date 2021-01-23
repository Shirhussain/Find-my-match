# Generated by Django 3.1.5 on 2021-01-22 17:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked_users', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_users', to=settings.AUTH_USER_MODEL, verbose_name='Liked users')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liker', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'UserLike',
                'verbose_name_plural': 'UserLikes',
            },
        ),
    ]