# Generated by Django 5.0.6 on 2024-06-27 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('future_app', '0008_remove_staff_email_remove_staff_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='designation',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
