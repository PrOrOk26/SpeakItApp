from django.db.models import (
    CharField, EmailField,
    DateField, BooleanField,
    Model, ManyToManyField,
    ManyToManyField, ManyToOneRel, 
)

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, 
)

class CustomUserManager(BaseUserManager):

    def create_user(self, username, password=None):
        if not username:
            raise ValueError("Username must be specified!")
        user = self.model(
            username=self.username,
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

class Language(Model):
    pass

class LangUser(AbstractBaseUser):
    username = CharField(
        verbose_name='Username',
        max_length=255,
        primary_key=True,
        unique=True,
    )
    first_name = CharField(verbose_name="First name",max_length=255,)
    last_name = CharField(verbose_name="Last name",max_length=255,)
    country = CharField(verbose_name="Country",max_length=255,)
    email = EmailField(
        verbose_name='Email address',
        max_length=255,
    )
    date_of_birth = DateField(verbose_name="Date of birth")
    languages = ManyToManyField(Language, through='UserLearnsLanguage')

    is_active = BooleanField(default=True)
    is_admin = BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['username', 'password', ]

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return f"{self.first_name}"

    def save(self, *args, **kwargs):
        super(LangUser, self).save(*args, **kwargs)

class UserLearnsLanguage(Model):
    pass

class Word(Model):
    pass
