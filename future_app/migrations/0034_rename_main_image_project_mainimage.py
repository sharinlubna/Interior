# Generated by Django 5.0.6 on 2024-08-03 12:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('future_app', '0033_project_image1_project_image2_project_image3_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='main_image',
            new_name='mainimage',
        ),
    ]
