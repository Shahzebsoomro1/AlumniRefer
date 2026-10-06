from django import forms
from .models import JobPosting

INPUT_CLASS = 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all bg-gray-50 focus:bg-white'
TEXTAREA_CLASS = INPUT_CLASS + ' resize-none'
SELECT_CLASS = INPUT_CLASS


class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = [
            'title', 'company', 'location', 'employment_type',
            'experience_level', 'description', 'requirements',
            'skills_required', 'salary_range', 'application_deadline'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'e.g. Senior Backend Engineer',
                'class': INPUT_CLASS
            }),
            'company': forms.TextInput(attrs={
                'placeholder': 'e.g. Acme Corp',
                'class': INPUT_CLASS
            }),
            'location': forms.TextInput(attrs={
                'placeholder': 'e.g. New York or Remote',
                'class': INPUT_CLASS
            }),
            'employment_type': forms.Select(attrs={'class': SELECT_CLASS}),
            'experience_level': forms.Select(attrs={'class': SELECT_CLASS}),
            'description': forms.Textarea(attrs={
                'rows': 6,
                'placeholder': 'Describe the role, responsibilities, and team...',
                'class': TEXTAREA_CLASS
            }),
            'requirements': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'List key requirements and qualifications...',
                'class': TEXTAREA_CLASS
            }),
            'skills_required': forms.TextInput(attrs={
                'placeholder': 'Python, Django, React, AWS',
                'class': INPUT_CLASS
            }),
            'salary_range': forms.TextInput(attrs={
                'placeholder': '$80,000 – $120,000',
                'class': INPUT_CLASS
            }),
            'application_deadline': forms.DateInput(attrs={
                'type': 'date',
                'class': INPUT_CLASS
            }),
        }
