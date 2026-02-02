from django.urls import include, path

from . import views
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers

routers = routers.DefaultRouter()
routers.register(r'', views.UserViewSet, basename='user')  

app_name = 'users'

urlpatterns = [
    path('', include(routers.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)