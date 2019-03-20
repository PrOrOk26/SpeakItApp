from django.urls import path

from . import views
from django.contrib.auth.views import LogoutView 

app_name = 'test_voc'

urlpatterns = [
    path('', views.test_main, name='testmain'),
]
