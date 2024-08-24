# Generated by Django 5.0.6 on 2024-08-05 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('future_app', '0037_project_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='description',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='category',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
