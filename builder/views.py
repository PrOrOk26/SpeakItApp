from django_tables2 import RequestConfig
from lang.models import Word, User
from .tables import WordsTable
from .forms import WordForm
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from .filters import WordFilter
from django.views.generic import (CreateView, ListView, 
                                    UpdateView, FormView,
                                    DetailView, TemplateView
)
from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages


class FilteredWordsListView(SingleTableMixin, FilterView):
    table_class = WordsTable
    queryset = None
    template_name = 'builder/builder.html'
    filterset_class = WordFilter 

    def get(self, request, username):
        self.queryset = Word.objects.filter(lang_id=request.user.languages.get(lang_name='English').id)
        filter_ = self.filterset_class(request.GET, queryset=self.queryset)
        table = self.table_class(filter_.qs)
        RequestConfig(request).configure(table)
        return render(request, 'builder/builder.html', {'table': table,
                                                        'filter': filter_})

class AddWordView(CreateView):
    template_name = 'builder/add_word.html'
    form_class = WordForm

    def get(self, request, username):
        form = self.form_class()
        return render(request, AddWordView.template_name, context={'form': form})

    def post(self, request, username):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            form.save(user=request.user)
            return HttpResponseRedirect(reverse("lang:builder:addword",
                                                kwargs={'username': username  }))
        messages.error(request, "Invalid data!")
        return render(request, AddWordView.template_name, context={'form': form})

class EditWordView(UpdateView):
    pass

class DeleteWordView(TemplateView):
    
    def post(self, request, username):
        word_id = request.POST.get('word', None)
        data = {
            'is_deleted': False
        }
        result = Word.objects.get(id=word_id).delete()
        if result[0] == 1:
            data['is_deleted'] = True
        return JsonResponse(data)

