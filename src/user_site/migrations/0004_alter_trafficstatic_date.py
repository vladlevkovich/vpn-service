# Generated by Django 4.2.7 on 2023-11-16 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_site', '0003_alter_trafficstatic_date_userstatistics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trafficstatic',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
