from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Announcement

User = get_user_model()


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        exclude = ['author']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'condition': forms.Select(attrs={'class': 'form-select'}),
            'image_ur': forms.URLInput(attrs={'class': 'form-control'}),
        }


# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = [field.name for field in User._meta.fields if field.name not in ['last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined']]
#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'form-control'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control'}),
#             # Добавь другие поля по необходимости
#         }

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')