from django import forms
from .models import Post, Comment


class PostAddForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "image", "caption")


class CommentAddForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)
