from django import forms
from django.core.exceptions import ValidationError
from .models import Mail

class mailForms(forms.ModelForm):
    class Meta:
        model = Mail
        fields = [
            'mail'
        ]

        widgets = {
            'mail': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First Name'}),
        }