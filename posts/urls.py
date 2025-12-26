from django.urls import path
from . import views

urlpatterns = [
    path('creating_post/', views.create_post_view, name='post_creating')
]
