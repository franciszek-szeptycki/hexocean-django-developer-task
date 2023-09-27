from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CustomUser, AccountTier
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from .serializers import LoginSerializer

@api_view(['POST'])
def login_view(request):

    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    user = serializer.validated_data['user']
    token, _ = Token.objects.get_or_create(user=user)

    return Response({'token': token.key})




