# Generated by Django 3.2.7 on 2021-10-01 06:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0015_user_imageurl'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='imageurl',
        ),
    ]