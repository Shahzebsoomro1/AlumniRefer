from django import forms
from .models import ReferralRequest

TEXTAREA_CLASS = 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all bg-gray-50 focus:bg-white resize-none'
SELECT_CLASS = 'w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all bg-gray-50 focus:bg-white'


class ReferralRequestForm(forms.ModelForm):
    class Meta:
        model = ReferralRequest
        fields = ['cover_note']
        widgets = {
            'cover_note': forms.Textarea(attrs={
                'rows': 6,
                'placeholder': 'Introduce yourself and explain why you are a strong candidate for this role. Be specific about your experience and how it aligns with the job requirements...',
                'class': TEXTAREA_CLASS,
                'maxlength': 1000,
            })
        }
        labels = {
            'cover_note': 'Cover Note'
        }


class AlumniResponseForm(forms.ModelForm):
    class Meta:
        model = ReferralRequest
        fields = ['status', 'alumni_note']
        widgets = {
            'status': forms.Select(
                choices=[('accepted', 'Accept'), ('rejected', 'Reject')],
                attrs={'class': SELECT_CLASS}
            ),
            'alumni_note': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Optional: Leave a note for the requester...',
                'class': TEXTAREA_CLASS,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].choices = [
            ('accepted', 'Accept Referral Request'),
            ('rejected', 'Decline Referral Request'),
        ]
        self.fields['alumni_note'].required = False


class AdminOutcomeForm(forms.ModelForm):
    class Meta:
        model = ReferralRequest
        fields = ['admin_outcome', 'admin_notes']
        widgets = {
            'admin_outcome': forms.Select(attrs={'class': SELECT_CLASS}),
            'admin_notes': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Internal notes (not visible to users)...',
                'class': TEXTAREA_CLASS,
            }),
        }
