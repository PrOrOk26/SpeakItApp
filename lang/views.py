from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User

from .forms import SignInForm, SignUpForm

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

def main(request, login):
    pass

def about(request):
    pass



