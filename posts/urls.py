from django.urls import path

from core import settings
from . import views

from django.conf.urls.static import static

app_name = 'posts'

urlpatterns = [
    path('post_creating/', views.create_post_view, name='post_creating'),
    path('post/<int:id>/', views.post_view, name='post_view'),
    path('like/<int:id>/', views.Like, name='like_post'),
    path('<int:post_id>', views.prev_post, name='prev_post'),
    path('next/<int:post_id>', views.next_post, name='next_post'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)