from django.contrib import admin
from .models import CustomUser, AccountTier, Thumbnail, Image
from django.db import models
from django_json_widget.widgets import JSONEditorWidget
from .models import validate_json_format

admin.site.register([CustomUser, Thumbnail, Image])

@admin.register(AccountTier)
class AccountTierAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget, 'validators': [validate_json_format]},
    }
