from django import forms
from .models import CustomUser, CustomerUserProfile, TheatreUserProfile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class CustomUserCreationForm(UserCreationForm):
    user_type = forms.CharField(widget=forms.HiddenInput(), initial="customer")

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2"]


class CustomerUserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerUserProfile
        fields = ["phone_number", "city"]


class TheatreUserProfileForm(forms.ModelForm):
    class Meta:
        model = TheatreUserProfile
        fields = ["name", "location"]


class CustomUserLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "password"]
