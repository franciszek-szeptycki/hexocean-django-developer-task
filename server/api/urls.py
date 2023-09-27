from django.urls import path
from .views import login_view, image_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', login_view),
    path('image/', image_view),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)