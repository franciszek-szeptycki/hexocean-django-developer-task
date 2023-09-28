from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Image
import os, uuid
from django.core.exceptions import ValidationError
from .functions import create_thumbnail, get_full_url, format_image_instance


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
        fields = ('image', 'user', 'thumbnail_links')
        extra_kwargs = {'image': {'required': True}}

    def validate_user(self, user):
        if not user.account_tier:
            raise ValidationError("User has no account tier.")
        return user
    
    def validate_image(self, image):
        if not image:
            raise ValidationError("No image provided.")

        ext = os.path.splitext(image.name)[1]
        if ext.lower() not in ('.png', '.jpg',):
            raise ValidationError("Unsupported file extension. Upload a .png or .jpg file.")
        return image

    def create(self, validated_data):
        image = validated_data.get('image')
        user = validated_data.get('user')
        
        ext = os.path.splitext(image.name)[1]
        image.name = f"{uuid.uuid4()}{ext}"

        instance = Image.objects.create(image=image, user=user, thumbnail_links=[])

        links = [create_thumbnail(instance, size, ext) for size in user.account_tier.thumbnail_size]
        instance.thumbnail_links = links

        return instance
        

class ImageListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ('image', )

    def get_image(self, instance):
        return get_full_url(instance)
