from django import forms
from .models import Post, UserProfile, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('published_date',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'location', 'birth_date']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Напишіть ваш коментар...'
            }),
        }
