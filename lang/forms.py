from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelForm

class SignInForm(forms.Form):
    username = forms.CharField(label="Login", min_length=5)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False), label="Password", min_length=5)

    def log_in(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user

class SignUpForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(render_value=False), label="confirmPassword", min_length=5)
    
    class Meta:
        model = User
        fields = ("username", "password", "email", )
        widgets = {
            "password": forms.PasswordInput(render_value=False),
        }

    def sign_up(self):
        try:
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')
            email = self.cleaned_data.get('email')
            user_check = User.objects.get(username=username)
            return None
        except ObjectDoesNotExist:
            user_check = User.objects.create_user(username=username,
            password=password,
            email=email)
            return user_check
        
