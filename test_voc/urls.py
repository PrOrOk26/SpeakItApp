from django.urls import path

from . import views

app_name = 'test_voc'

urlpatterns = [
    path('', views.TestMainView.as_view(), name='testmain'),
    path('test_meanings/', views.TestMeaningView.as_view(), name='testmeaning'),
    path('test_meanings/get_questions/', views.TestQuestionsSupplierView.as_view(), name='testquestionsupplier')
]
