# Generated by Django 5.0.6 on 2024-06-26 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('future_app', '0006_alter_staff_designation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='designation',
            field=models.IntegerField(choices=[(1, 'Architect'), (2, 'Interior Designer'), (3, 'Project Manager'), (4, 'Design Consultant'), (5, 'Draftsperson'), (6, 'Lighting Designer'), (7, 'Furniture Designer'), (8, 'Materials Specialist'), (9, '3D Visualizer'), (10, 'Site Supervisor'), (11, 'Procurement Manager'), (12, 'Client Relations Manager'), (13, 'Junior Interior Designer'), (14, 'Senior Interior Designer'), (15, 'Administrative Assistant')], default=1),
        ),
    ]
