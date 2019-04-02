from django.shortcuts import render
from django.contrib.auth.views import LogoutView 
from django.contrib.auth.views import PasswordChangeView, TemplateView
from django.http import HttpResponseRedirect, JsonResponse
from lang.models import Word, WordExample, WordQuestion, WordSynonim

from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import (CreateView, ListView, 
                                    UpdateView, FormView,
                                    DetailView,
)
from django.db.models import Max
from random import randint

class TestMainView(TemplateView):
    template_name = "test_voc/test_main.html"

    def get(self, request, username):
        return render(request, TestMainView.template_name)

class TestMeaningView(TemplateView):
    template_name = "test_voc/test_meaning.html"

    def get(self, request, username):
        return render(request, TestMeaningView.template_name)

class TestQuestionsSupplierView(TemplateView):

    def get(self, request, username):
        tests_number = request.GET.get('tests', None)
        data = {'tests': []}
        data['tests'] = self.create_meanings_tests(request.user, tests_number, 'English')
        return JsonResponse(data)
    

    def create_meanings_tests(self, user, tests_numb, language, meanings_amount=4,
                                examples_amount=1):
        max_word_id = Word.objects.filter(lang_id=user.languages.get(lang_name=language).id).aggregate(max_id=Max(id))['max_id']
        tests = []
        words_gen = 0
        words_id = []
        while words_gen != tests_numb:
            rand_pk = randint(1, max_word_id)
            word = Word.objects.filter(id=rand_pk).first()
            if word and rand_pk not in words_id:
                words_gen += 1
                words_id.append(rand_pk)
                meanings = [word.meaning_set.first().meaning]
                for i in range(meanings_amount - 1):
                    rand_pk = randint(1, max_word_id)
                    meanings.append(Word.objects.filter(id=rand_pk).first().meaning_set.first().meaning)
                examples = word.word_example_set
                if len(examples) >= examples_amount:
                    examples = [examples[i].text for i in range(examples_amount)]
                else:
                    examples = [examples[i].text for i in range(len(examples))]
                tests.append({'word': word.word,
                              'question': word.word_question_set.first(),
                              'right_meaning': meanings[0],
                              'word_meanings': meanings[1:],
                              'word_examples': examples})
                continue
        return tests
        

