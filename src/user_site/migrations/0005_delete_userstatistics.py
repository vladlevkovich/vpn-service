# Generated by Django 4.2.7 on 2023-11-17 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_site', '0004_alter_trafficstatic_date'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserStatistics',
        ),
    ]