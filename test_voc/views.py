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
<<<<<<< HEAD
        max_word_id = Word.objects.filter(lang_id=user.languages.get(lang_name=language).id).aggregate(max_id=Max('id'))['max_id']
        words = Word.objects.filter(lang_id=user.languages.get(lang_name=language).id)
        
        tests = []
        words_gen = 0
        words_id = []

        tests_numb = int(tests_numb)

        while words_gen != tests_numb:
            rand_pk = randint(1, max_word_id)
            word = words.filter(id=rand_pk).first()
            meanings = []

            if word and rand_pk not in words_id:
                words_id.append(rand_pk)
                if word.meaning_set.count() != 0:
                    meanings = [word.meaning_set.first().meaning]
                    words_gen += 1
                else:
                    continue

                while len(meanings) != meanings_amount:
                    rand_pk = randint(1, max_word_id)
                    word_to_get_meaning = words.filter(id=rand_pk).first()

                    if word_to_get_meaning and word_to_get_meaning.meaning_set.count() > 0:
                        while True:
                            meanings_count = word_to_get_meaning.meaning_set.count()
                            rand_meaning_number = None
                            if meanings_count > 1:
                                rand_meaning_number = randint(0, word_to_get_meaning.meaning_set.count() - 1)
                            else:
                                rand_meaning_number = 0

                            meaning_to_append = word_to_get_meaning.meaning_set.first().meaning
                            if meaning_to_append in meanings:
                                break
                            if meaning_to_append:
                                meanings.append(meaning_to_append)
                                break
                
                examples = word.wordexample_set
                if not examples:
                    examples = []
                elif examples.count() >= examples_amount:
                    examples = [example.text for example in examples.all()[:examples_amount]]
                else:
                    examples = [example.text for example in examples.all()]
                tests.append({'word_id': word.id,
                              'word': word.word,
=======
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
>>>>>>> e87c545f01ef9f8b019a93407d61e4eb88a5b33f
                              'right_meaning': meanings[0],
                              'word_meanings': meanings[1:],
                              'word_examples': examples})
                continue
        return tests
        

