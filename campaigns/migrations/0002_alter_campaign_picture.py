# Generated by Django 5.1.4 on 2024-12-11 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='campaign_images'),
        ),
    ]
