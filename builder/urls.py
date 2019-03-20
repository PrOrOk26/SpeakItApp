from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'builder'
LANG_APP = 'lang.urls'
BUILDER_APP = 'builder.urls'

urlpatterns = [
    path('', views.FilteredWordsListView.as_view(), name='builder_main'),
    path('add/', views.AddWordView.as_view(), name='addword'),
    path('edit/<str:word>', views.EditWordView.as_view(), name='editword'),
    path('delete/', views.DeleteWordView.as_view(), name='deleteword')
]