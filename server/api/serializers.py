from django.contrib.auth import authenticate
from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    data['user'] = user
                else:
                    raise serializers.ValidationError("User is deactivated.")
            else:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")
        
        return data
