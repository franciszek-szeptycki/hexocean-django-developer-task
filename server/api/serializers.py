from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Image, ExpiringLink
import os, uuid
from django.core.exceptions import ValidationError
from .functions import create_thumbnail
from datetime import datetime, timedelta


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
        fields = ('id', 'image', 'user', 'thumbnail_links')
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
    
    def to_representation(self, instance):
        return {
            "original": self.context['request'].build_absolute_uri(instance.image.url),
            "thumbnails": [self.context['request'].build_absolute_uri(link) for link in instance.thumbnail_links]
        }
        

class ImageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image', )


class ExpiringLinkSerializer(serializers.ModelSerializer):
    time = serializers.IntegerField(write_only=True)

    class Meta:
        model = ExpiringLink
        fields = ('image_id', 'time', 'token',)

    def validate_time(self, value: int):
        time_delta = timedelta(seconds=value)
        target_time = datetime.now() + time_delta
        
        min_time = datetime.now() + timedelta(seconds=300)
        max_time = datetime.now() + timedelta(seconds=30_000)

        if not min_time < target_time:
            raise serializers.ValidationError(f"Minimum expiration time is 300 seconds.")
        elif not target_time < max_time:
            raise serializers.ValidationError(f"Maximum expiration time is 30,000 seconds.")
        return target_time
    
    def create(self, validated_data):
        token = uuid.uuid4()
        image_id = validated_data.get('image_id')
        expiration_time = validated_data.get('time')

        return ExpiringLink.objects.create(token=token, image_id=image_id, expiration_time=expiration_time)
    
    def to_representation(self, instance):
        return {
            'link': f"{self.context['request'].build_absolute_uri('/')}{instance.token}"
        }
