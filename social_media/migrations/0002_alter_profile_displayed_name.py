# Generated by Django 4.2.9 on 2024-02-04 10:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("social_media", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="displayed_name",
            field=models.CharField(max_length=60, unique=True),
        ),
    ]
