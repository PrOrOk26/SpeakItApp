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
from random import randint, choice
from django.template.loader import render_to_string
from json import loads

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
                              'right_meaning': meanings[0],
                              'word_meanings': meanings[1:],
                              'word_examples': examples})
                continue
        return tests

class TestProcessResultView(TemplateView):
    phrases_success = ("Great job!You are getting better with every test!",
                        "Well done!You will be speaking even better with such results",
                        "Here we go!That's how you do it!")
    phrases_failure = ("Bad!You need to have more practise!",
                        "You should have done this test better!")
    phrases_medium = ("OK!But you can do better!",
                       "Not bad,but this is not best result possible!",
                        "Not your best, but you can do better next time!")

    def post(self, request, username):
        test_results = loads(request.POST.get("results")) 
        right_answers = 0

        for result in test_results:
            word = Word.objects.get(id=result.get("word_id"))
            word_right = word.success_rate * word.times_asked
            word_right += result['times_right']
            word.times_asked += result['times_asked']
            word.success_rate = word_right / word.times_asked
            word.save()
            
            right_answers += result['times_right']
        
        result_to_show = {
            'times_right': right_answers,
            'times_asked': len(test_results),
            'phrase': "",
            'header': "",
        }

        if right_answers < int(len(test_results) / 2):
            result_to_show['phrase'] = choice(self.phrases_failure)
            result_to_show['header'] = "Bad,but your results will be better!"
        elif right_answers in range(int(len(test_results) / 2), int(len(test_results) * 0.8)):
            result_to_show['phrase'] = choice(self.phrases_medium)
            result_to_show['header'] = "Not bad, but you are able to improve even more!"
        elif right_answers in range(int(len(test_results) * 0.8), len(test_results)):
            result_to_show['phrase'] = choice(self.phrases_success)
            result_to_show['header'] = "Good result, but there is no limit to perfection!"
        elif right_answers == len(test_results):
            result_to_show['phrase'] = "Your result is perfect in this test,but don't stop learning!"
            result_to_show['header'] = "Excellent result, no wrong answers!"
        
        resultHTML = render_to_string('test_voc/test_results.html', request=request, 
                                context=result_to_show)
        return JsonResponse({'resultHTML': resultHTML })
        

