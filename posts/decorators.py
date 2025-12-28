from django.shortcuts import get_object_or_404

from django import req

from .models import Post

def post_required(view_func):
    def wrapper(request, *args, **kwargs):
        post_id = kwargs.get('id')
        post = get_object_or_404(Post, id=post_id)
        return view_func(request ,*args, **kwargs, post=post)
    return wrapper