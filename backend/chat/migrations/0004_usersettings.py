# Generated by Django 5.1.4 on 2024-12-30 15:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_chathistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reminders_enabled', models.BooleanField(default=True)),
                ('reminder_time', models.TimeField(blank=True, null=True)),
                ('reminder_message', models.TextField(default="Don't forget to take a break!")),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
