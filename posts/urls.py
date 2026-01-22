from django.urls import include, path

from core import settings
from .views import PostDetailedView, CreatePostView
from . import views
from rest_framework import routers

from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='posts')
router.register(r'comments', views.CommentViewSet, basename='comments')

app_name = 'posts'

urlpatterns = [
    path('post_creating/', CreatePostView.as_view(), name='post_creating'),
    path('post/<str:username>/<int:pk>/', PostDetailedView.as_view(), name='post_view'),
    path('like/<int:id>/', views.like_post, name='like_post'),
    path('prev/<str:username>/<int:post_id>/', views.prev_post, name='prev_post'),
    path('next/<str:username>/<int:post_id>/', views.next_post, name='next_post'),
    path('feed/', views.feed_view, name='feed'),
    path('comments/<int:pk>/', views.post_comments_view, name='comments_view'),
    path('like_comment/<int:pk>', views.like_comment, name='like_comment'),
    path('delete/comment/<int:pk>/', views.delete_comment, name='delete_comment'),
    path('delete/post/<int:id>/', views.delete_post, name='delete_post'),

    path('api/', include(router.urls)),
    

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)