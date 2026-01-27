from django.urls import include, path

from core import settings
from . import views
from rest_framework import routers

from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='posts')
router.register(r'comments', views.CommentViewSet, basename='comments')

app_name = 'posts'

urlpatterns = [
    path('api/', include(router.urls)),
    

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)