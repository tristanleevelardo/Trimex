import re
from django import forms
from django.core.exceptions import ValidationError
from .models import unit

class unitForms(forms.ModelForm):
    class Meta:
        model = unit
        fields = [

            'subject', 'course','instructor_firstName','instructor_lastName',
        ]

        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Subject'}),
            'course': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Section'}),
            'instructor_firstName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Instructor First Name'}),
            'instructor_lastName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Instructor Last Name'}),
        }


    def clean_subject(self):
        subject = self.cleaned_data.get('subject')
        return subject.capitalize()

    def clean_instructor_firstName(self):
        instructor_firstName = self.cleaned_data.get('instructor_firstName')
        return instructor_firstName.capitalize()

    def clean_instructor_lastName(self):
        instructor_lastName = self.cleaned_data.get('instructor_lastName')
        return instructor_lastName.capitalize()

    def clean_section(self):
        section = self.cleaned_data.get('course')
        return section.upper()
