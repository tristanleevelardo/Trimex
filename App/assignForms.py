import re
from django import forms
from django.core.exceptions import ValidationError
from .models import thirdYear

class ThirdYearFormAssign(forms.ModelForm):
    class Meta:
        model = thirdYear
        fields = [
            'student_firstName', 'student_lastName',
            'subject', 'course',
            'instructor_firstName', 'instructor_lastName',
        ]

        widgets = {
            'student_firstName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First Name'}),
            'student_lastName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Last Name'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Subject'}),
            'course': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Section'}),
            'instructor_firstName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Instructor First Name'}),
            'instructor_lastName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Instructor Last Name'}),
        }

    def clean_student_firstName(self):
        student_firstName = self.cleaned_data.get('student_firstName')
        return student_firstName.capitalize()

    def clean_student_lastName(self):
        student_lastName = self.cleaned_data.get('student_lastName')
        return student_lastName.capitalize()

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
