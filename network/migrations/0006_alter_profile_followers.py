# Generated by Django 3.2.7 on 2021-09-27 14:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_rename_follower_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='followers',
            field=models.ManyToManyField(blank=True, null=True, related_name='followerlist', to=settings.AUTH_USER_MODEL),
        ),
    ]
