from django.db import models
from django.utils.timezone import now

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,
    PermissionsMixin 
)


class CustomUserManager(BaseUserManager):

    def create_user(self, username=None, password=None, **kwargs):
        if not username:
            raise ValueError("Username must be specified!")
        user = self.model(
            username=username,
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password, **kwargs):
        user = self.create_user(
            username=username,
            password=password,
            is_superuser=True,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class Language(models.Model):
    lang_name = models.CharField(max_length=255,) 

    def __str__(self):
        return self.lang_name

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        verbose_name='Username',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(verbose_name="First name",max_length=255,)
    last_name = models.CharField(verbose_name="Last name",max_length=255,)
    country = models.CharField(verbose_name="Country",max_length=255,)
    email = models.EmailField(
        verbose_name='Email address',
        max_length=255,
    )
    date_of_birth = models.DateField(verbose_name="Date of birth", null=True,)
    languages = models.ManyToManyField(Language, through='UserLearnsLanguage')

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password', ]

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return f"{self.first_name}"

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        

class UserLearnsLanguage(models.Model):
    lang_id = models.ForeignKey(Language, on_delete=models.CASCADE)
    learner_id = models.ForeignKey(User, on_delete=models.CASCADE)
    started_learning = models.DateTimeField(default=now())

    def __str__(self):
        return f'{self.learner_id} learns {self.lang_id}'

class Topic(models.Model):
    topic_name = models.CharField(max_length=255)
    topic_desc = models.CharField(max_length=255, )
    success_rate = models.FloatField(default=0.0)
    language_id = models.ForeignKey(Language, on_delete=models.CASCADE)

    def __str__(self):
        return self.topic_name


class Word(models.Model):
    ADJECTIVE = 'ADJ'
    NOUN = 'N'
    VERB = 'V'
    PREPOSITION = 'PREP'
    ADVERB = 'ADV'
    PARTS_GRAMMAR_CHOICES = (
        (ADJECTIVE, 'Adjective'),
        (NOUN, 'Noun'),
        (VERB, 'Verb'),
        (PREPOSITION, 'Preposition'),
        (ADVERB, 'Adverb'),
    )
    
    word = models.CharField(max_length=255)
    grammar_part = models.CharField(choices=PARTS_GRAMMAR_CHOICES,
                                    default=NOUN,
                                    max_length=255)
    success_rate = models.FloatField(default=0.0)
    times_asked = models.IntegerField(default=0)
    date_created = models.DateTimeField("Created At", auto_now_add=True, editable=False)
    topics = models.ManyToManyField(Topic, through='WordHasTopic')
    lang_id = models.ForeignKey(Language, on_delete=models.CASCADE)
    student_id = models.ForeignKey(UserLearnsLanguage, on_delete=models.CASCADE)

    def __str__(self):
        return self.word

class WordHasTopic(models.Model):
    topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.word} has a topic {self.topic_id}"

class Meaning(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    meaning = models.CharField(max_length=255)
    guide_word = models.CharField(max_length=255)

    def __str__(self):
        return self.meaning


class WordSynonim(models.Model):
    meaning_id = models.ForeignKey(Meaning, on_delete=models.CASCADE)
    word_id = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='word_id')
    synonym_word_id = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='synonym_word_id')

    def __str__(self):
        return f'{self.word_id} has synonym {self.synonym_word_id}'

class WordExample(models.Model):
    meaning_id = models.ForeignKey(Meaning, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class WordQuestion(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text
