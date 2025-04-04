# Generated by Django 5.1.7 on 2025-03-23 01:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0002_timeslot'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='priority',
            field=models.PositiveIntegerField(default=1, help_text='Priorité pour la planification automatique'),
        ),
        migrations.AddField(
            model_name='course',
            name='rd_color',
            field=models.CharField(default='#378006', help_text='Couleur de la carte', max_length=20),
        ),
        migrations.CreateModel(
            name='ManualSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manual_sessions', to='resources.course')),
            ],
        ),
    ]
