# Generated by Django 4.2.12 on 2024-06-30 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journals', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='municipality',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='personal_number',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='postal_code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
