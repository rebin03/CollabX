# Generated by Django 5.1.4 on 2025-01-04 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0006_alter_campaign_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('completed', 'Completed'), ('pending', 'Pending'), ('working', 'Working'), ('completed', 'Completed'), ('closed', 'Closed')], default='Active', max_length=10),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='Pending', max_length=20),
        ),
    ]
