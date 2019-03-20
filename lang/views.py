from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView, TemplateView

from .forms import (SignInForm, SignUpForm, UserEditForm, 
                    AddUserLearnsLanguageForm)
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import (CreateView, ListView, 
                                    UpdateView, FormView,
                                    DetailView,
)

from .models import Word, User, UserLearnsLanguage, Language

from django.contrib.auth.decorators import login_required

HTML_INDEX = 'lang/index.html'
HTML_ABOUT = ''
HTML_SIGN_IN = 'lang/signin.html'
HTML_SIGN_UP = 'lang/signup.html'
HTML_MAIN = 'lang/main.html'
PAGE_INDEX = '/index'
PAGE_ABOUT = ''
PAGE_SIGN_IN = '/signin'
PAGE_SIGN_UP = '/signup'

def index(request):
    return render(request, HTML_INDEX)

def sign_in(request):
    sign_in_form = SignInForm(request.POST or None)
    if request.method == 'POST' and sign_in_form.is_valid():
        user = sign_in_form.log_in(request)
        if user:
            login(request, user)
            return HttpResponseRedirect("/{}/main/".format(user.get_username()))
        messages.error(request, "Invalid login or password")
    return render(request, HTML_SIGN_IN, {'form': sign_in_form})


def sign_up(request):
    sign_up_form = SignUpForm(request.POST or None)
    if request.method == 'POST' and sign_up_form.is_valid():
        user = sign_up_form.sign_up()
        if user:
            return HttpResponseRedirect(PAGE_SIGN_IN)
        messages.error(request, "Error signing up user!")
    return render(request, HTML_SIGN_UP, {'form': sign_up_form})

@login_required
def main(request, username):
    return render(request,HTML_MAIN, {'username': username} )

@login_required
def about(request):
    pass

class ProfileView(DetailView):
    form_class = UserEditForm
    template_name = "lang/profile.html"
    context_object_name = 'user'  

    def get(self, request, username):
        profile_form = self.form_class(instance=request.user)
        return render(request, 'lang/profile.html', context={'form': profile_form})

    def post(self, request, username):
        profile_form = self.form_class(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            return HttpResponseRedirect("/{}/main/".format(username))
        messages.error(request, "Invalid data!")
        return render(request, 'lang/profile.html', context={'form': profile_form})
        

    def get_object(self):
        _username = self.kwargs.get('username')
        user = get_object_or_404(User, username=_username)
        return user

class LangPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = "lang/edit_password.html"   

    def get(self, request, username):
        profile_form = self.form_class(user=request.user)
        return render(request, LangPasswordChangeView.template_name, context={'form': profile_form})

    def post(self, request, username):
        profile_form = self.form_class(data=request.POST, user=request.user)
        if profile_form.is_valid():
            profile_form.save()
            update_session_auth_hash(request, profile_form.user)
            return HttpResponseRedirect("/{}/profile/".format(username))
        messages.error(request, "Invalid data!")
        return render(request, LangPasswordChangeView.template_name, context={'form': profile_form})
        

    def get_object(self):
        _username = self.kwargs.get('username')
        user = get_object_or_404(User, username=_username)
        return user

class BuilderView(TemplateView):
    template_name = "lang/builder.html"

    def get(self, request, username):
        return render(request, BuilderView.template_name)

class LearningCabinetView(TemplateView):
    template_name = "lang/learning_cabinet.html"
    form_class = AddUserLearnsLanguageForm

    def get(self, request, username):
        user = request.user
        languages_learning = user.languages.all()
        languages_to_learn = Language.objects.all().difference(languages_learning)
        form = self.form_class(languages=languages_to_learn)
        return render(request, LearningCabinetView.template_name, context={'languages': languages_learning,
                                                            'form': form})

    def post(self, request, username):
        user = request.user
        language = request.POST.get('languages')[0]
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect("/{}/main/".format(username))
