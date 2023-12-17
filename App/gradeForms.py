from django import forms
from .models import thirdYear

class ThirdYearForm(forms.ModelForm):
    class Meta:
        model = thirdYear
        fields = [
            'totalSW', 'totalQuiz', 'performanceTask', 'prelim', 'midterm', 'finals'
        ]

        widgets = {
            'totalSW': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'min': 0, 'max': 100}),
            'totalQuiz': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'min': 0, 'max': 100}),
            'performanceTask': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'min': 0, 'max': 100}),
            'prelim': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'min': 0, 'max': 100}),
            'midterm': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'min': 0, 'max': 100}),
            'finals': forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'min': 0, 'max': 100}),
        }
