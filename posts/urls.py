from django.urls import include, path

from core import settings
from . import views
from rest_framework import routers
    

from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'', views.PostViewSet, basename='post')
router.register(r'comments', views.CommentViewSet, basename='comment')

app_name = 'posts'

urlpatterns = [
    path('', include(router.urls)),
    

]