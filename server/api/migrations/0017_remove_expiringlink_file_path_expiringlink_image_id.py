# Generated by Django 4.2.5 on 2023-10-03 18:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0016_expiringlink"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="expiringlink",
            name="file_path",
        ),
        migrations.AddField(
            model_name="expiringlink",
            name="image_id",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="expiring_links",
                to="api.image",
            ),
        ),
    ]
