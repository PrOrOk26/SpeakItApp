from django_tables2 import RequestConfig
from lang.models import Word, User, UserLearnsLanguage, Language
from .tables import WordsTable
from .forms import WordForm, UserTopicsFormset
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from .filters import WordFilter
from django.views.generic import (CreateView, ListView, 
                                    UpdateView, FormView,
                                    DetailView, TemplateView
)
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

class FilteredWordsListView(SingleTableMixin, FilterView):
    table_class = WordsTable
    queryset = None
    template_name = 'builder/builder.html'
    filterset_class = WordFilter 

    def get(self, request, username):
        self.queryset = Word.objects.filter(lang_id=request.user.languages.get(lang_name='English').id)
        filter_ = self.filterset_class(request.GET, queryset=self.queryset)
        table = self.table_class(filter_.qs)
        RequestConfig(request, paginate={'per_page': 10}).configure(table)
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
    model = Word
    template_name = 'builder/update_word_form.html'
    form_class = WordForm
    success_url = reverse_lazy('lang:builder:builder_main')

    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Word, id=pk)

    def post(self, request, username, pk):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            form.save(user=request.user, word_pk=pk)
            return HttpResponseRedirect(reverse("lang:builder:builder_main",
                                                kwargs={'username': username  }))
        messages.error(request, "Invalid data!")
        return render(request, EditWordView.template_name, context={'form': form})

class DeleteWordView(TemplateView):
    
    def post(self, request, username):
        word_id = request.POST.get('word', None)
        data = {
            'is_deleted': False
        }
        result = Word.objects.get(id=word_id).delete()
        if 1 in result:
            data['is_deleted'] = True
        return JsonResponse(data)

class ManageTopicsView(ListView):

    template_name = "builder/add_topic.html"
    
    def get(self, request, username):
        language_learner = UserLearnsLanguage.objects.get(learner_id=request.user, 
                                     lang_id=Language.objects.get(
                                         lang_name='English'))
        formset = UserTopicsFormset(queryset=language_learner.topic_set.order_by('?'))
        return render(request, self.template_name, {'formset': formset})

    def post(self, request, username):
        language_learner = UserLearnsLanguage.objects.get(learner_id=request.user, lang_id=Language.objects.get(lang_name='English'))
        formset = UserTopicsFormset(request.POST)
        if formset.is_valid():
            for topic_form in formset:
                if topic_form.is_valid():
                    if topic_form not in formset.deleted_forms:
                        topic_form.save(commit=True,
                                language_learner=language_learner
                                )
                    else:
                        topic = topic_form.save(commit=False,
                                        language_learner=language_learner)
                        topic.delete()

            return HttpResponseRedirect(reverse("lang:builder:builder_main",
                                                kwargs={'username': username  }))
        messages.error(request, "Invalid data!")
        return render(request, ManageTopicsView.template_name, context={'formset': formset})

