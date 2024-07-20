# Generated by Django 5.0.6 on 2024-07-11 22:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('future_app', '0019_appointment_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='user_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_id', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
