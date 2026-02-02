from urllib import request
from django.shortcuts import render, redirect

from users.serializers import UserSerializer
from .forms import RegisterForm, EditProfileForm

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .models import CustomUser, Follow

from django.db.models import Count, Exists, OuterRef

from posts.models import Post

from django.views.generic import DetailView

from django.shortcuts import get_object_or_404



from rest_framework import viewsets, permissions

def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if(request.method=='POST'):
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    return render(request, 'users/login_view.html',{'form': form})

def register_view(request):
    form = RegisterForm(request.POST, request.FILES)

    if(request.method=='POST'):
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
        return redirect('home')
    return render(request, 'users/register_view.html', {'form': form})


def profile_view(request, username, profile_user):
    posts = Post.objects.filter(author=profile_user)

    context = {
        'profile_user': profile_user, 
        'is_following': Follow.objects.filter(from_user=request.user, to_user=profile_user).exists(),
        'followers_count': profile_user.followers_count(), 
        'following_count': profile_user.following_count(),
        'posts': posts.select_related('author').annotate(likes_count=Count('likes')),
        }

    return render(request, 'users/profile_view.html', context)

def profile_edit(request):
    user = request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users:profile', username=user.username)
    else:
        form = EditProfileForm(instance=user)
    return render(request, 'users/edit_profile.html', {'form': form})

def members_list_view(request):
    users = CustomUser.objects.annotate(is_following=Exists(Follow.objects.filter(from_user=request.user, to_user=OuterRef('pk'))))
    return render(request, 'users/members_list.html', {'users': users})

def logout_view(request):
    if request.method == "GET":
        logout(request)
        return redirect('home')

def following(request , username, profile_user):
    if(request.method == 'POST'):
        if not Follow.objects.filter(from_user=request.user, to_user=profile_user).exists():
            Follow.objects.create(from_user=request.user, to_user=profile_user)
        return redirect('users:profile', username=profile_user.username)

def unfollowing(request, username, profile_user):
    if(request.method=='POST'):
        if Follow.objects.filter(from_user=request.user, to_user=profile_user).exists():
            Follow.objects.filter(from_user=request.user, to_user=profile_user).delete()
        return redirect('users:profile', username=profile_user.username)
    
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        user = self.request.user
        queryset = CustomUser.objects.all().annotate(
            following_count = Count('following', distinct=True),
            followers_count = Count('followers', distinct=True),
            post_count = Count('posts', distinct=True),
            is_followed=Exists(Follow.objects.filter(
                from_user=user, to_user=OuterRef('pk')
        )
        )
        )
        return queryset