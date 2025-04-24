from django import forms
from django.forms import PasswordInput

class OTPForm(forms.Form):
    otp = forms.CharField(
        label='OTP',
        max_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter the OTP'
        })
    )

class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(
        label='New Password',
        widget=PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter new password'
        }),
        min_length=8,  # Minimum length for security
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Confirm new password'
        }),
        min_length=8,  # Minimum length for security
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        # Check if the passwords match
        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        # Optional: Additional checks for password complexity can be added here
        if len(new_password) < 8:  # Example: Minimum length
            raise forms.ValidationError("Password must be at least 8 characters long.")


class ExcelUploadForm(forms.Form):
    file = forms.FileField()