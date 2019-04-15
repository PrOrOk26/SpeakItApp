from django_tables2 import RequestConfig
from lang.models import (Word, User, UserLearnsLanguage, Language,
                        Meaning, WordExample)
from .tables import WordsTable
from .forms import (WordForm, UserTopicsFormset, WordMeaningsFormset,
                    WordExamplesFormset)
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

class ManageTopicsView(TemplateView):

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

class ManageMeaningsView(TemplateView):
    template_name = "builder/edit_word_meanings.html"
    
    def get(self, request, username):
        pk = request.GET.get('pk' or None)
        meanings_to_edit = Meaning.objects.filter(word=pk).order_by('?')
        formset = WordMeaningsFormset(queryset=meanings_to_edit)
        return render(request, self.template_name, {'formset': formset,
                                                    'pk': pk})

    def post(self, request, username):
        pk = request.GET.get('pk' or None)
        word = Word.objects.get(id=pk)
        formset = WordMeaningsFormset(request.POST)
        if formset.is_valid():
            for meaning_form in formset:
                if meaning_form.is_valid():
                    if meaning_form not in formset.deleted_forms:
                        meaning_form.save(commit=True,
                                word=word)
                    else:
                        meaning = meaning_form.save(commit=False,
                                        word=word)
                        meaning.delete()

            return HttpResponseRedirect(reverse("lang:builder:builder_main",
                                                kwargs={'username': username  }))
        messages.error(request, "Invalid data!")
        return render(request, ManageMeaningsView.template_name, context={'formset': formset})


class ManageExamplesView(TemplateView):
    template_name = "builder/edit_word_examples.html"
    
    def get(self, request, username):
        pk = request.GET.get('pk' or None)
        examples_to_edit = WordExample.objects.filter(word=pk).order_by('?')
        formset = WordExamplesFormset(queryset=examples_to_edit)
        return render(request, self.template_name, {'formset': formset,
                                                    'pk': pk})

    def post(self, request, username):
        pk = request.GET.get('pk' or None)
        word = Word.objects.get(id=pk)
        formset = WordExamplesFormset(request.POST)
        if formset.is_valid():
            for example_form in formset:
                if example_form.is_valid():
                    if example_form not in formset.deleted_forms:
                        example_form.save(commit=True,
                                word=word
                                )
                    else:
                        example = example_form.save(commit=False,
                                        word=word)
                        example.delete()

            return HttpResponseRedirect(reverse("lang:builder:builder_main",
                                                kwargs={'username': username  }))
        messages.error(request, "Invalid data!")
        return render(request, ManageExamplesView.template_name, context={'formset': formset})
