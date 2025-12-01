from django.urls import path

from .views import profile_view, register_view, login_view, profile_settings, members_list_view, logout_view, following, unfollowing
from django.conf.urls.static import static
from django.conf import settings


app_name = 'users'

urlpatterns = [
    path('profile/user/<int:pk>/', profile_view, name='profile'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('profile/settings/', profile_settings, name="profile_edit"),
    path('members/', members_list_view, name="members_list"),
    path('logout/', logout_view, name='logout'),
    path('follow/<int:pk>', following, name='following'),
    path('unfollow/<int:pk>', unfollowing, name='unfollowing'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)