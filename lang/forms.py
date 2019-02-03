from django import forms
from django.contrib.auth import authenticate
from .models import LangUser
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelForm
from django.core.validators import MinLengthValidator

class SignInForm(forms.ModelForm):

    class Meta:
        model = LangUser
        fields = ("username", "password", )

    def __init__(self, *args, **kwargs):
        super(SignInForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput(
                render_value=False,
                )
        self.fields['username'].validators.append(MinLengthValidator(limit_value=5))
        self.fields['password'].validators.append(MinLengthValidator(limit_value=5))

    def log_in(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user

class SignUpForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(render_value=False), label="confirmPassword", min_length=5)
    
    class Meta:
        model = LangUser
        fields = ("username", "password", "email", )

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput(
                render_value=False,
                )
        self.fields['username'].validators.append(MinLengthValidator(limit_value=5))
        self.fields['password'].validators.append(MinLengthValidator(limit_value=5))
        self.fields['confirm_password'].validators.append(MinLengthValidator(limit_value=5))
        

    def sign_up(self):
        try:
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')
            email = self.cleaned_data.get('email')
            user_check = LangUser.objects.get(username=username)
            return None
        except ObjectDoesNotExist:
            user_check = LangUser.objects.create_user(username=username,
            password=password, )
            user_check.email = email
            user_check.save()
            return user_check
        
