# Generated by Django 4.2.5 on 2023-10-03 17:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0014_alter_image_image_alter_thumbnail_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="accounttier",
            name="expiring_link",
            field=models.BooleanField(default=False),
        ),
    ]
