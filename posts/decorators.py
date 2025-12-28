from django.shortcuts import get_object_or_404

from .models import Post

def post_required(view_func):
    def wrapper(request, *args, **kwargs):
        id = kwargs.get('id')
        post = get_object_or_404(Post, id=id)
        return view_func(request, *args, post=post, **kwargs)
    return wrapper