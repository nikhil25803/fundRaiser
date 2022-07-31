from django import forms
from .models import PostModel


class NewPostForm(forms.ModelForm):

    class Meta:

        model = PostModel

        fields = [
            'title', 'heading', 'description', 'upi_id', 'image',
        ]

        labels = {
            'title': 'Title of the Post',
            'heading': 'Post heading',
            'description': 'Describe your post',
            'upi_id': 'Your UPI ID for the payment',
            'images': 'Upload an image',
        }

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control m-1'}),

            'heading': forms.TextInput(attrs={'class': 'form-control m-1'}),

            'description': forms.TextInput(attrs={'class': 'form-control m-1'}),

            'upi_id': forms.TextInput(attrs={'class': 'form-control m-1'}),

        }

    pass
