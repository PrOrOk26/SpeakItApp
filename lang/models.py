from django.db import models
from django.utils.timezone import now

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, 
)


class CustomUserManager(BaseUserManager):

    def create_user(self, username=None, password=None):
        if not username:
            raise ValueError("Username must be specified!")
        user = self.model(
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password):
        user = self.create_user(
            username=username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class Language(models.Model):
    lang_name = models.CharField(max_length=255,)
    started_learning = models.DateTimeField(default=now())

class User(AbstractBaseUser):
    username = models.CharField(
        verbose_name='Username',
        max_length=255,
        primary_key=True,
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
    
    word = models.CharField(max_length=255,)
    grammar_part = models.CharField(choices=PARTS_GRAMMAR_CHOICES,
                                    default=NOUN,
                                    max_length=255,
    )
    date_created = models.DateTimeField(default=now())
    lang_id = models.ForeignKey(Language, on_delete=models.CASCADE)
    student_id = models.ForeignKey(UserLearnsLanguage, on_delete=models.CASCADE)


class Meaning(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    meaning = models.CharField(max_length=255)
    guide_word = models.CharField(max_length=255)
    
