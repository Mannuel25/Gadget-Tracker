from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label=("Enter a password"), strip=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label=("Password Confirmation"), strip=False, widget=forms.PasswordInput)

    class Meta:
        fields = ('email', 'full_name')
        model = CustomUser

class StaffVendorForm(UserChangeForm):
    class Meta:
        fields = ['full_name', 'staff_id', 'email', 'phone_no', 'address', 'picture']
        model = CustomUser

class UserForm(forms.ModelForm):
    class Meta:
        fields = ['full_name', 'staff_id', 'user_type', 'email', 'phone_no', 'address', 'level', 'department', 'picture']
        model = CustomUser

