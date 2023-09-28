from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image as PILImage
import sys, io, uuid
from .models import Thumbnail


def __create(instance, size, format):
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


def create_thumbnails(instance, sizes, format):
    return [ __create(instance, size, format) for size in sizes ]

