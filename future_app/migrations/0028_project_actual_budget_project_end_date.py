# Generated by Django 5.0.6 on 2024-07-23 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('future_app', '0027_alter_appointment_status_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='actual_budget',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
