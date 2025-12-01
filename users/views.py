from urllib import request
from django.shortcuts import render, redirect

from .forms import RegisterForm

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .models import CustomUser


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
    return render(request, 'users/profile_view.html', {'profile_user': profile_user})

def profile_settings(request):
    return render(request, 'users/edit_profile.html')

def members_list_view(request):
    users = CustomUser.objects.all()
    return render(request, 'users/members_list.html', {'users': users})

def logout_view(request):
    if request.method == "GET":
        logout(request)
        return redirect('home')