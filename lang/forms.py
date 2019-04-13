from django import forms
from django.contrib.auth import authenticate
from .models import User
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelForm
from django.core.validators import MinLengthValidator
from django.contrib.auth.forms import UserChangeForm


class SignInForm(forms.Form):

    username = forms.CharField(label='Username',
                validators=[MinLengthValidator(limit_value=5)],
                )
    password = forms.CharField(widget=forms.PasswordInput(
                render_value=False,
                ), label='Password',
                validators=[MinLengthValidator(limit_value=5),
                ])

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
            user_check = User.objects.get(username=username)
            return None
        except ObjectDoesNotExist:
            user_check = User.objects.create_user(username=username,
            password=password, )
            user_check.email = email
            user_check.save()
            return user_check
    
class UserEditForm(UserChangeForm):
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 
                    'last_name', 'country', 'date_of_birth',
                    )

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].widget = forms.DateInput()
        self.fields['date_of_birth'].help_text = "For example: 1999-01-26"
        self.fields['email'].help_text = "Valid email address"
        self.fields['country'].help_text = "The country you live in"
        self.fields['password'].help_text = "You can change your password using the button below"

 
    def save(self, commit=True):
        user = super(UserEditForm, self).save(commit=False)
        user.country = self.cleaned_data.get('country')
        user.date_of_birth = self.cleaned_data.get('date_of_birth')

        if commit:
            user.save()
        
        return user

class AddUserLearnsLanguageForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('languages',)
        widgets = {'languages': forms.Select}
    
    def __init__(self, *args, **kwargs):
        languages = kwargs.pop('languages', None)
        super(AddUserLearnsLanguageForm, self).__init__(*args, **kwargs)
        if languages:
            self.fields['languages'].queryset = languages

    def save(self, commit=True):
        user = super(AddUserLearnsLanguageForm, self).save(commit=False)

        if commit:
            user.save()
        
        return user
