# Generated by Django 5.2 on 2025-04-15 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memberships', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
