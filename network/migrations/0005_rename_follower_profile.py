# Generated by Django 3.2.7 on 2021-09-27 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_follower_imageurl'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Follower',
            new_name='Profile',
        ),
    ]