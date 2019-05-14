# Generated by Django 2.1.5 on 2019-05-14 19:04

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=255, unique=True, verbose_name='Username')),
                ('first_name', models.CharField(max_length=255, verbose_name='First name')),
                ('last_name', models.CharField(max_length=255, verbose_name='Last name')),
                ('country', models.CharField(max_length=255, verbose_name='Country')),
                ('email', models.EmailField(max_length=255, verbose_name='Email address')),
                ('date_of_birth', models.DateField(null=True, verbose_name='Date of birth')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lang_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Meaning',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meaning', models.CharField(max_length=255)),
                ('guide_word', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_name', models.CharField(max_length=255)),
                ('topic_desc', models.CharField(blank=True, default='', max_length=255)),
                ('success_rate', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='UserLearnsLanguage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started_learning', models.DateTimeField(default=datetime.datetime(2019, 5, 14, 19, 4, 2, 236921, tzinfo=utc))),
                ('lang_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lang.Language')),
                ('learner_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=255)),
                ('grammar_part', models.CharField(choices=[('ADJ', 'Adjective'), ('N', 'Noun'), ('V', 'Verb'), ('PREP', 'Preposition'), ('ADV', 'Adverb')], default='N', max_length=255)),
                ('success_rate', models.FloatField(default=0.0)),
                ('times_asked', models.IntegerField(default=0)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('lang_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lang.Language')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lang.UserLearnsLanguage')),
            ],
        ),
        migrations.CreateModel(
            name='WordExample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
                ('meaning_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lang.Meaning')),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lang.Word')),
            ],
        ),
        migrations.CreateModel(
            name='WordHasTopic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lang.Topic')),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lang.Word')),
            ],
        ),
        migrations.CreateModel(
            name='WordQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lang.Word')),
            ],
        ),
        migrations.CreateModel(
            name='WordSynonim',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meaning_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lang.Meaning')),
                ('synonym_word_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='synonym_word_id', to='lang.Word')),
                ('word_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='word_id', to='lang.Word')),
            ],
        ),
        migrations.AddField(
            model_name='word',
            name='topics',
            field=models.ManyToManyField(through='lang.WordHasTopic', to='lang.Topic'),
        ),
        migrations.AddField(
            model_name='topic',
            name='language_learner_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lang.UserLearnsLanguage'),
        ),
        migrations.AddField(
            model_name='meaning',
            name='word',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lang.Word'),
        ),
        migrations.AddField(
            model_name='user',
            name='languages',
            field=models.ManyToManyField(through='lang.UserLearnsLanguage', to='lang.Language'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
