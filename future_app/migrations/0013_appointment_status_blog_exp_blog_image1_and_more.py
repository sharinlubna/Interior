# Generated by Django 5.0.6 on 2024-07-05 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('future_app', '0012_blog'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='status',
            field=models.IntegerField(choices=[(1, 'Scheduled'), (2, 'Rejected')], default=1),
        ),
        migrations.AddField(
            model_name='blog',
            name='exp',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='image1',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='blog',
            name='sub_title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='date',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='time',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
