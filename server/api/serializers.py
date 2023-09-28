from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Image, Thumbnail
from PIL import Image as PILImage
import os, io, uuid, sys


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            raise serializers.ValidationError("Must include 'username' and 'password'.")
        
        user = authenticate(request=self.context.get('request'), username=username, password=password)
            
        if user is None:
            raise serializers.ValidationError("Unable to log in with provided credentials.")
        
        if not user.is_active:
            raise serializers.ValidationError("User is deactivated.")
        
        data['user'] = user
        return data


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

    def validate_user(self, value):
        if value.account_tier is None:
            raise serializers.ValidationError("User has no account tier.")
        return value


    def validate_image(self, value):
        if value is None:
            raise serializers.ValidationError("Must include 'image'.")

        ext = os.path.splitext(value.name)[1]
        valid_extensions = ['.jpg', '.png']
        
        if not ext.lower() in valid_extensions:
            raise serializers.ValidationError('Unsupported file extension. Upload a .jpg or .png file.')
        
        return value
    

    def create(self, validated_data):

        image = validated_data.get('image')
        user = validated_data.get('user')
        
        ext = os.path.splitext(image.name)[1]
        unique_name = f"{uuid.uuid4()}{ext}"
        image.name = unique_name

        instance = Image.objects.create(image=image, user=user, thumbnail_links=[])

        thumbnails_data = user.account_tier.thumbnail_size
        thumbnail_links = []

        for thumbnail_data in thumbnails_data:
            thumbnail = PILImage.open(image)

            width = thumbnail_data.get('width') or sys.maxsize
            height = thumbnail_data.get('height') or sys.maxsize
            
            thumbnail.thumbnail((width, height))

            thumb_io = io.BytesIO()
            thumbnail.save(thumb_io, format='PNG')
            
            thumbnail_file = InMemoryUploadedFile(
                thumb_io, None, f"{uuid.uuid4()}{ext}", 'image/png',
                thumb_io.getbuffer().nbytes, None
            )
            
            thumbnail_instance = Thumbnail.objects.create(original=instance, image=thumbnail_file, width=width, height=height)
            
            thumbnail_links.append(thumbnail_instance.image.url)
        
        instance.thumbnail_links = thumbnail_links
        instance.save()
        return instance