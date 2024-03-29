# Generated by Django 4.2.9 on 2024-02-04 19:10

from django.db import migrations, models
import social_media.models


class Migration(migrations.Migration):
    dependencies = [
        ("social_media", "0002_alter_profile_displayed_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="followers",
            field=models.ManyToManyField(
                related_name="following",
                through="social_media.Follow",
                to="social_media.profile",
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="profile_pic",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=social_media.models.profile_pic_file_path,
            ),
        ),
    ]
