from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Announcement, ExchangeProposal

User = get_user_model()


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        exclude = ['author']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'condition': forms.Select(attrs={'class': 'form-select'}),
            'image_ur': forms.URLInput(attrs={'class': 'form-control'}),
        }
class ExchangeProposalForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ['comment']
        widgets = {
            
            'comment': forms.Textarea(attrs={'class': 'form-control',
                                             'rows': 4}),
            
        }


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')