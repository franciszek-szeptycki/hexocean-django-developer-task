# Generated by Django 4.2.5 on 2023-09-27 19:12

import api.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0006_alter_accounttier_thumbnail_size"),
    ]

    operations = [
        migrations.RenameField(
            model_name="customuser",
            old_name="my_model",
            new_name="account_tier",
        ),
        migrations.AlterField(
            model_name="accounttier",
            name="thumbnail_size",
            field=models.JSONField(validators=[api.validators.validate_json_format]),
        ),
    ]
