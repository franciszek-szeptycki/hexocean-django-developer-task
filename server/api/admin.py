import os, json
from django.contrib import admin
from django.db import models
from django.contrib.auth.models import Group
from django.conf import settings
from django_json_widget.widgets import JSONEditorWidget
from .models import CustomUser, AccountTier, Thumbnail, Image, ExpiringLink
from .validators import validate_json_format


# Load initial account tiers used to prevent editing or deleting them
file_path = os.path.join(settings.BASE_DIR, 'fixtures.json')
with open(file_path, 'r') as file:
    data = json.load(file)
restricted_names = [item["fields"]["name"] for item in data]


admin.site.register([CustomUser, Thumbnail, Image, ExpiringLink])
admin.site.unregister(Group)


@admin.register(AccountTier)
class AccountTierAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget, 'validators': [validate_json_format]},
    }

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.name in restricted_names:
            return [field.name for field in obj._meta.fields]
        return super().get_readonly_fields(request, obj=obj)
