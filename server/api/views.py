from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import LoginSerializer, ImageSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
def login_view(request):

    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    user = serializer.validated_data['user']
    token, _ = Token.objects.get_or_create(user=user)

    return Response({'token': token.key})


@api_view(['POST', 'GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def image_view(request):

    user = request.user

    if request.method == 'POST':
        data = request.data.copy()
        data['user'] = user.id
        serializer = ImageSerializer(data=data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data)
    
    if request.method == 'GET':
        images = user.images.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)
