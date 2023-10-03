from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image as PILImage
from .models import Thumbnail
from rest_framework import serializers
import sys, io, uuid, os, dotenv
from .models import CustomUser, Image


def create_thumbnail(instance, size, format):
    tmb = PILImage.open(instance.image.path)
    width = size.get('width') or sys.maxsize
    height = size.get('height') or sys.maxsize
    
    tmb.thumbnail((width, height))

    thumb_io = io.BytesIO()
    tmb.save(thumb_io, format='PNG')
    
    tmb_file = InMemoryUploadedFile(
        thumb_io, None, f"{uuid.uuid4()}{format}", 'image/png',
        thumb_io.getbuffer().nbytes, None
    )
    
    return Thumbnail.objects.create(original=instance, image=tmb_file, width=width, height=height).image.url


# dotenv.load_dotenv()
# DOMAIN = os.getenv('DOMAIN')
# SSL = os.getenv('SSL') == 'True'

# def get_full_link(url):
#     link = "http"
#     if SSL:
#         link += "s"
#     link += "://" + DOMAIN + url
#     return link


# def format_image_instance(instance):
#     data = {
#         'thumbnail_links': [get_full_link(link) for link in instance["thumbnail_links"]]
#     }
#     if CustomUser.objects.filter(id=instance["user"]).first().account_tier.original_link:
#         data['image'] = get_full_link(instance["image"])
    
#     return data
