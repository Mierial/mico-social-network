from urllib import request
from django.shortcuts import render, redirect

from .forms import RegisterForm, EditProfileForm

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .models import CustomUser, Follow

from django.shortcuts import get_object_or_404


def login_view(request):
    form = AuthenticationForm(request, data=request.POST)

    if(request.method=='post'):
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        return render(request, 'users/login_view.html',{'form': form})

def register_view(request):
    form = RegisterForm(request.POST, request.FILES)

    if(request.method=='post'):
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
        return redirect('home.html', {'user': user})
    else:
        return render(request, 'users/register_view.html', {'form': form})

def profile_view(request, username):
    profile_user = get_object_or_404(CustomUser, username=username)
    return render(request, 'users/profile_view.html', {
        'profile_user': profile_user, 
        'is_following': profile_user.is_following(request.user), 
        'followers_count': profile_user.followers_count(), 
        'following_count': profile_user.following_count(),
        })

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
    users = CustomUser.objects.all()
    return render(request, 'users/members_list.html', {'users': users})

def logout_view(request):
    if request.method == "GET":
        logout(request)
        return redirect('home')
    
def following(request , username):
    profile_user = get_object_or_404(CustomUser, username=username)
    if(request.method == 'POST'):
        if not Follow.objects.filter(from_user=request.user, to_user=profile_user).exists():
            Follow.objects.create(from_user=request.user, to_user=profile_user)
        return redirect('users:profile', username=profile_user.username)

def unfollowing(request, username):
    profile_user = get_object_or_404(CustomUser, username=username)
    if(request.method=='POST'):
        if Follow.objects.filter(from_user=request.user, to_user=profile_user).exists():
            Follow.objects.filter(from_user=request.user, to_user=profile_user).delete()
        return redirect('users:profile', username=profile_user.username)