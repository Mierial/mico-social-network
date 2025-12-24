from django.urls import path

from . import views
from django.conf.urls.static import static
from django.conf import settings


app_name = 'users'

urlpatterns = [
    path('profile/user/<str:username>/', views.profile_view, name='profile'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/edit/', views.profile_edit, name="profile_edit"),
    path('members/', views.members_list_view, name="members_list"),
    path('logout/', views.logout_view, name='logout'),
    path('follow/<str:username>/', views.following, name='following'),
    path('unfollow/<str:username>/', views.unfollowing, name='unfollowing'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)