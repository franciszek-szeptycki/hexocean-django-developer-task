# Generated by Django 4.2.5 on 2023-10-03 15:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0013_accounttier_original_link_alter_image_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="image",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="original/"),
        ),
        migrations.AlterField(
            model_name="thumbnail",
            name="image",
            field=models.ImageField(upload_to="thumbnails/"),
        ),
    ]