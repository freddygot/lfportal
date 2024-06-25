# Generated by Django 5.0.6 on 2024-06-25 18:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kurs', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modul',
            name='innhold',
        ),
        migrations.AddField(
            model_name='modul',
            name='beskrivelse',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='modul',
            name='kurs',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moduler', to='kurs.kurs'),
        ),
        migrations.CreateModel(
            name='FullfortKurs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullfort_dato', models.DateTimeField(auto_now_add=True)),
                ('bruker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('kurs', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kurs.kurs')),
            ],
        ),
    ]
