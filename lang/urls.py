from django.urls import path

from . import views
from django.contrib.auth.views import LogoutView 

app_name = 'lang'
urlpatterns = [
    path('', views.index, name='index'),
    path('signin/', views.sign_in, name='signin'),
    path('signup/', views.sign_up, name='signup'),
    path('about/', views.about, name='about'),
    path('<str:username>/main/', views.main, name='main'),
    path('<str:username>/profile/', views.ProfileView.as_view(), name='profile'),
    path('<str:username>/profile/change-password/', views.LangPasswordChangeView.as_view(),name='changepassword'),
    path('<str:username>/logout/', LogoutView.as_view(), name='logout'),
]

