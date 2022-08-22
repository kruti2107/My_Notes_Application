from django.forms import ModelForm
from .models import User, Note
from django import forms


class RegistrationSerializer(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']


class NotesSerializer(ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'description', 'favourite']
        exclude = ['user']
        widgets = {
            'description': forms.Textarea()
        }