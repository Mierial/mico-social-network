from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Post, Likes
from .decorators import post_required

def create_post_view(request):
    form = PostForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('users:profile', username=request.user.username)
    return render(request, 'posts/post_creating.html', {'form': form})

def post_view(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'posts/post_page.html', {'post_id': id, 'post': post})

@post_required
def Like(request, post):
    if request.method == 'POST':
        Likes.objects.create(post, user=request.user)
    
    