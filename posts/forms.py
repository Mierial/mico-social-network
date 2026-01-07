from django import forms

from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={
                'class': 'form-control bg-secondary text-white border-0 rounded-pill',
                'placeholder': 'Додати коментар...',
                'style': 'box-shadow: none;'  
            })
        }