# Generated by Django 5.1.4 on 2024-12-18 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_creatorprofile_follower_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creatorprofile',
            name='follower_count',
            field=models.FloatField(),
        ),
    ]
