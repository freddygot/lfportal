# Generated by Django 4.2.12 on 2024-06-29 21:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('journals', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('personal', models.IntegerField()),
                ('interpersonal', models.IntegerField()),
                ('social', models.IntegerField()),
                ('general', models.IntegerField()),
                ('total_score', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='journals.appointment')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='journals.client')),
            ],
        ),
    ]