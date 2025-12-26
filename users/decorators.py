from .models import CustomUser
from django.shortcuts import get_object_or_404, redirect, render

from urllib import request

def profile_user_required(view_func):
    def wrapper(request, *args, **kwargs):
        username = kwargs.get('username')
        profile_user = get_object_or_404(CustomUser, username=username)
        return view_func(request, *args, profile_user=profile_user, **kwargs)
    return wrapper

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        return redirect('users:login')
    return wrapper