from urllib import request
from django.shortcuts import render, redirect

from .forms import RegisterForm

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .models import CustomUser, Follow


def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('home')
    return render(request, 'users/login_view.html',{'form': form})

def register_view(request):
    form = RegisterForm(request.POST, request.FILES or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return render(request, 'core/home.html', {'user': user})
    return render(request, 'users/register_view.html', {'form': form})

def profile_view(request, pk):
    profile_user = CustomUser.objects.get(pk=pk)
    is_following = Follow.objects.filter(from_user=request.user, to_user=profile_user).exists()
    followers_count = Follow.objects.filter(to_user=profile_user).count()
    following_count = Follow.objects.filter(from_user=profile_user).count()
    return render(request, 'users/profile_view.html', {'profile_user': profile_user, 'is_following': is_following, 'followers_count': followers_count, 'following_count': following_count})

def profile_settings(request):
    return render(request, 'users/edit_profile.html')

def members_list_view(request):
    users = CustomUser.objects.all()
    return render(request, 'users/members_list.html', {'users': users})

def logout_view(request):
    if request.method == "GET":
        logout(request)
        return redirect('home')
    
def following(request, pk):
    profile_user = CustomUser.objects.get(pk=pk)
    if(request.method == 'POST'):
        Follow.objects.create(from_user=request.user, to_user=profile_user)
    return redirect('users:profile', pk=pk)

def unfollowing(request, pk):
    profile_user = CustomUser.objects.get(pk=pk)
    if(request.method=='POST'):
        Follow.objects.filter(from_user=request.user, to_user=profile_user).delete()
    return redirect('users:profile', pk=pk)