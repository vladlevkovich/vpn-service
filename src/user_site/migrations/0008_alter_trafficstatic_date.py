# Generated by Django 4.2.7 on 2023-11-17 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_site', '0007_trafficstatic_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trafficstatic',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
