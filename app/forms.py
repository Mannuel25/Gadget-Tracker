from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from .models import Gadget, CustomUser, UploadedTemplates
from django.forms import BaseInlineFormSet, HiddenInput

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label=("Enter a password"), strip=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label=("Password Confirmation"), strip=False, widget=forms.PasswordInput)

    class Meta:
        fields = ('email', 'full_name')
        model = CustomUser

class UserForm(forms.ModelForm):

    user_id = forms.CharField(max_length=20, label="Matric number/Staff ID/Vendor ID")
    class Meta:
        model = CustomUser
        fields = ['full_name', 'user_id', 'user_type', 'email', 'phone_no', 'address', 'level', 'department', 'picture']
        widgets = {
            'full_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'required': True
                    }
                ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
        }

class GadgetForm(forms.ModelForm):
    class Meta:
        model = Gadget
        fields = ['model', 'color', 'device_id', 'missing']


class CustomGadgetFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(CustomGadgetFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.fields['DELETE'].widget = HiddenInput()

GadgetFormSet = inlineformset_factory(CustomUser, Gadget, form=GadgetForm, extra=1, can_delete=True, can_delete_extra=True, formset=CustomGadgetFormSet)


class UploadedTemplatesForm(forms.ModelForm):
    class Meta:
        model = UploadedTemplates
        fields = ['doc']

