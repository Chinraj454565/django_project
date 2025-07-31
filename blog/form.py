from .models import Comment
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        exclude=['post']
        labels={
            "user_name": "Your Name",
            "user_email": "Your Email"

        }


