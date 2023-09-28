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


class Image(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/original/', null=True, blank=True)
    thumbnail_links = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.image}"
    
class Thumbnail(models.Model):
    original = models.ForeignKey(Image, on_delete=models.CASCADE, default=None)
    image = models.ImageField(upload_to='images/thumbnails/')
    width = models.IntegerField()
    height = models.IntegerField()

    def __str__(self):
        return f"{self.image} - {self.width}x{self.height}"