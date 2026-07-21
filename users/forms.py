from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["bio", "avatar"]


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254,help_text="Required. Enter a valid email address.")
    class Meta:
        model = User
        fields = ("username","email","password1","password2")


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Username or email"
    