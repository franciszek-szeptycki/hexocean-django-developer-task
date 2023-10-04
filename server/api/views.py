from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import LoginSerializer, ImageSerializer, ImageListSerializer, ExpiringLinkSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import ExpiringLink, Image
from django.utils import timezone
from django.http import HttpResponse


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
        serializer = ImageSerializer(data=data, context={'request': request})

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    
    if request.method == 'GET':
        images = Image.objects.filter(user=user).order_by('-id')
        serializers = ImageSerializer(images, many=True, context={'request': request})
        return Response(image for image in serializers.data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_link_view(request):

    serializer = ExpiringLinkSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data)


@api_view(['GET'])
def token_view(_, token):

    link = ExpiringLink.objects.filter(token=token).first()
    if not link:
        return Response({'error': 'Invalid token.'}, status=400)

    if link.expiration_time < timezone.now():
        link.delete()
        return Response({'error': 'Token expired.'}, status=400)
    
    image = Image.objects.filter(id=link.image_id.id).first()

    with open(image.image.path, 'rb') as f:
        return HttpResponse(f.read(), content_type="image/png")