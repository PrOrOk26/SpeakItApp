from lang.models import (Word, UserLearnsLanguage, 
                        Language, Topic, WordExample,
                        Meaning)
from django.core.exceptions import ObjectDoesNotExist
from django import forms
from django.core.validators import MinLengthValidator

class WordForm(forms.ModelForm):
    
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

class UserTopicsForm(forms.ModelForm):

    class Meta:
        model = Topic
        fields = ('topic_name', 'topic_desc', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['topic_name'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter topic name here'
        })
        self.fields['topic_desc'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter topic description here'
        })
        self.fields['topic_name'].validators.append(MinLengthValidator(limit_value=5))
        self.fields['topic_desc'].validators.append(MinLengthValidator(limit_value=5))

    def save(self, commit=False, language_learner=None):
        if not language_learner:
            return 
        topic = super(UserTopicsForm, self).save(commit=False)
        if not topic.pk and not topic.topic_name:
            return 
        topic.language_learner_id_id = language_learner.pk

        if commit:
            topic.save()
        
        return topic

class WordMeaningForm(forms.ModelForm):

    class Meta:
        model = Meaning
        fields = ('meaning', 'guide_word', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['meaning'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter meaning here'
        })
        self.fields['guide_word'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter guide word to enhance your learning process'
        })
        self.fields['meaning'].validators.append(MinLengthValidator(limit_value=3))
        self.fields['guide_word'].validators.append(MinLengthValidator(limit_value=3))

    def save(self, commit=False, word=None):
        if not word or word.id:
            return 
        meaning = super(WordMeaningForm, self).save(commit=False)
        meaning.word = word.id

        if commit:
            meaning.save()
        
        return meaning

class WordExamplesForm(forms.ModelForm):

    class Meta:
        model = WordExample
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your example here'
        })
        self.fields['text'].validators.append(MinLengthValidator(limit_value=5))

    def save(self, commit=False, word=None):
        if not word or word.id:
            return 
        example = super(WordExamplesForm, self).save(commit=False)
        example.word = word.id
        example.meaning_id = word.meaning_set.first().id

        if commit:
            example.save()
        
        return example

UserTopicsFormset = forms.modelformset_factory(Topic, form=UserTopicsForm, extra=1,
                                                can_delete=True)
WordMeaningsFormset = forms.modelformset_factory(Meaning, form=WordMeaningForm, extra=1,
                                                can_delete=True)
WordExamplesFormset = forms.modelformset_factory(WordExample, form=WordExamplesForm, extra=1,
                                                can_delete=True)