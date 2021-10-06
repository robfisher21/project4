# Generated by Django 3.2.7 on 2021-09-27 09:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_follower_posts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follower',
            name='followers',
            field=models.ManyToManyField(related_name='followerlist', to=settings.AUTH_USER_MODEL),
        ),
    ]