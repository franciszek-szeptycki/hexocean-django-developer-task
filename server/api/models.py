from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_json_format


class AccountTier(models.Model):
    name = models.CharField(max_length=100)
    thumbnail_size = models.JSONField(default=[{}] ,validators=[validate_json_format])

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    account_tier = models.ForeignKey(AccountTier, null=True, blank=True, on_delete=models.SET_NULL)