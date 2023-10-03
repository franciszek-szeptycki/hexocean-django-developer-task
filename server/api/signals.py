from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from .models import AccountTier

# @receiver(pre_save, sender=AccountTier)
# def prevent_edit_for_special_names(sender, instance, **kwargs):
#     if instance.pk:
#         original = sender.objects.get(pk=instance.pk)
#         if original.name in ["Premium", "Basic", "Enterprise"]:
#             raise ValidationError("Nie można edytować nazwy dla tego typu konta!")
