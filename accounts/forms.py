from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser, Profile


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Create a strong password',
            'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all bg-gray-50 focus:bg-white'
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password',
            'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all bg-gray-50 focus:bg-white'
        })
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'role']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'First name',
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all bg-gray-50 focus:bg-white'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Last name',
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all bg-gray-50 focus:bg-white'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'your@email.com',
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all bg-gray-50 focus:bg-white'
            }),
            'role': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all bg-gray-50 focus:bg-white'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only allow job_seeker and alumni to self-register
        self.fields['role'].choices = [
            ('job_seeker', 'Job Seeker'),
            ('alumni', 'Alumni'),
        ]
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords don't match.")
        return p2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email'].split('@')[0] + str(CustomUser.objects.count())
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'placeholder': 'your@email.com',
            'autofocus': True,
            'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all bg-gray-50 focus:bg-white'
        })
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password',
            'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all bg-gray-50 focus:bg-white'
        })
    )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'avatar', 'bio', 'company', 'job_title',
            'years_of_experience', 'linkedin_url',
            'skills', 'location', 'phone', 'is_accepting_referrals'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Tell others about yourself...',
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all bg-gray-50 focus:bg-white resize-none'
            }),
            'company': forms.TextInput(attrs={
                'placeholder': 'e.g. Google, Microsoft',
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all bg-gray-50 focus:bg-white'
            }),
            'job_title': forms.TextInput(attrs={
                'placeholder': 'e.g. Senior Software Engineer',
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all bg-gray-50 focus:bg-white'
            }),
            'years_of_experience': forms.NumberInput(attrs={
                'placeholder': '5',
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all bg-gray-50 focus:bg-white'
            }),
            'linkedin_url': forms.URLInput(attrs={
                'placeholder': 'https://linkedin.com/in/yourprofile',
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all bg-gray-50 focus:bg-white'
            }),
            'skills': forms.TextInput(attrs={
                'placeholder': 'Python, Django, React, PostgreSQL',
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all bg-gray-50 focus:bg-white'
            }),
            'location': forms.TextInput(attrs={
                'placeholder': 'New York, USA',
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all bg-gray-50 focus:bg-white'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': '+1 234 567 8900',
                'class': 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all bg-gray-50 focus:bg-white'
            }),
            'is_accepting_referrals': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-indigo-600 rounded border-gray-300 focus:ring-indigo-500'
            }),
        }
