# Generated by Django 3.2.7 on 2021-10-01 10:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0017_user_user_posts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='user_posts',
        ),
        migrations.AddField(
            model_name='profile',
            name='following',
            field=models.ManyToManyField(blank=True, null=True, related_name='following', to=settings.AUTH_USER_MODEL),
        ),
    ]
