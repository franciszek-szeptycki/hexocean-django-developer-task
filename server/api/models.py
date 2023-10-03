from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_json_format
import uuid


class AccountTier(models.Model):
    name = models.CharField(max_length=100)
    thumbnail_size = models.JSONField(default=[{}] ,validators=[validate_json_format])
    original_link = models.BooleanField(default=False)
    expiring_link = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    account_tier = models.ForeignKey(AccountTier, null=True, blank=True, on_delete=models.SET_NULL)


class Image(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='original/', null=True, blank=True)
    thumbnail_links = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.image}"
    

class Thumbnail(models.Model):
    original = models.ForeignKey(Image, on_delete=models.CASCADE, default=None)
    image = models.ImageField(upload_to='thumbnails/')
    width = models.IntegerField()
    height = models.IntegerField()

    def __str__(self):
        return f"{self.image} - {self.width}x{self.height}"
    

class ExpiringLink(models.Model):
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    image_id = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='expiring_links')
    expiration_time = models.DateTimeField()
