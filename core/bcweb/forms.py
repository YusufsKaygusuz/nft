from django import forms
from .models import Certificate, Company, User

class CertificateUploadForm(forms.ModelForm):
    # Add user-related fields
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    phone_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))

    class Meta:
        model = Certificate
        fields = ['verification_code', 'provider_company', 'file']
        widgets = {
            'verification_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter verification code'}),
            'provider_company': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
