from django.shortcuts import redirect, render

from .forms import PostForm

def create_post_view(request):
    user = request.user
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('users:profile', username=request.user.username)
    return render(request, 'posts/post_creating', {'form': form})