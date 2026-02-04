from urllib import request
from django.shortcuts import render, redirect

from users.serializers import UserListSerializer, UserDetailSerializer
from .forms import RegisterForm, EditProfileForm

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .models import CustomUser, Follow

from django.db.models import Count, Exists, OuterRef, Value, BooleanField

from posts.models import Post

from django.views.generic import DetailView

from django.shortcuts import get_object_or_404



from rest_framework import viewsets, permissions

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        return UserDetailSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = CustomUser.objects.all() 

        followers_count_subquery = Count('followers', distinct=True)

        if user.is_authenticated:
            is_followed_subquery = Exists(Follow.objects.filter(
                from_user=user,
                to_user=OuterRef('pk')
                )
            )
        else:
            is_followed_subquery = Value(False, output_field=BooleanField())

        if self.action == 'list':
            queryset = queryset.annotate(
                followers_count=followers_count_subquery,
                is_followed =  is_followed_subquery
                )
            
        if self.action == 'retrieve':
            queryset = queryset.annotate(
                following_count = Count('following', distinct=True),
                followers_count = followers_count_subquery,
                is_followed = is_followed_subquery,
                
                )
        return queryset
    