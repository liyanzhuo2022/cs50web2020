from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        labels = {
            'comment': 'Your Comment'
        }
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
        }