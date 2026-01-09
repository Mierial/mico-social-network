from django.urls import path

from core import settings
from .views import PostDetailedView, create_post_view
from . import views


from django.conf.urls.static import static

app_name = 'posts'

urlpatterns = [
    path('post_creating/', create_post_view.as_view(), name='post_creating'),
    path('post/<str:username>/<int:pk>/', PostDetailedView.as_view(), name='post_view'),
    path('like/<int:id>/', views.Like, name='like_post'),
    path('prev/<str:username>/<int:post_id>/', views.prev_post, name='prev_post'),
    path('next/<str:username>/<int:post_id>/', views.next_post, name='next_post'),
    path('feed/', views.feed_view, name='feed'),
    path('comments/<int:pk>/', views.post_comments_view, name='comments_view'),
    path('like_comment/<int:pk>', views.like_comment, name='like_comment'),
    path('delete/comment/<int:pk>/', views.delete_comment, name='delete_comment'),
    path('delete/post/<int:id>/', views.delete_post, name='delete_post')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)