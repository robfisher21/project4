# Generated by Django 3.2.7 on 2021-10-01 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0019_auto_20211001_1130'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='imageurl',
        ),
        migrations.AddField(
            model_name='user',
            name='imageurl',
            field=models.URLField(blank=True, max_length=1000, null=True),
        ),
    ]
