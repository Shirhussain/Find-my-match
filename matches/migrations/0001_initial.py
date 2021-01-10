# Generated by Django 3.1.5 on 2021-01-10 09:04

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
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_decimal', models.DecimalField(decimal_places=2, max_digits=16, verbose_name='Percentage')),
                ('question_answered', models.IntegerField(default=0, verbose_name='Answered Question')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Timestamp')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('user_a', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match_user_a', to=settings.AUTH_USER_MODEL, verbose_name='User A')),
                ('user_b', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match_user_b', to=settings.AUTH_USER_MODEL, verbose_name='User B')),
            ],
            options={
                'verbose_name': 'match',
                'verbose_name_plural': 'matchs',
            },
        ),
    ]
