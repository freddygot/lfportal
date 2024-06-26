# Generated by Django 5.0.6 on 2024-06-26 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_alter_profile_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='key_metrics',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('franchise_taker', 'Franchise-taker'), ('employee', 'Ansatt')], max_length=30),
        ),
    ]
