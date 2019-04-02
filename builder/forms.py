from lang.models import Word, UserLearnsLanguage, Language
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelForm

class WordForm(ModelForm):
    
    class Meta:
        model = Word
        fields = ('word', 'grammar_part', 'topics'
                    )

    def __init__(self, *args, **kwargs):
        super(WordForm, self).__init__(*args, **kwargs)
 
    def save(self, commit=True, user=None, word_pk=None):
        word = None
        if not word_pk:
            word = super(WordForm, self).save(commit=False)
        else:
            word = Word.objects.get(id=word_pk)
        word.grammar_part = self.cleaned_data.get('grammar_part')
        word.word = self.cleaned_data.get('word')
        word.lang_id = Language.objects.get(id=1)  # to fix, ADD 
        word.student_id = UserLearnsLanguage.objects.get(learner_id=user, lang_id=1)

        if commit:
            word.save()
        
        return word


