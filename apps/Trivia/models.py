from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings

import abc
import uuid 

from simple_history.models import HistoricalRecords
from taggit.managers import TaggableManager
from autoslug import AutoSlugField

class PublishedQuizManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(visibility='public')

class Quiz(models.Model):

    CHOICE_STATUS = (
        ('draft', 'Draft'),
        ('publish', 'Publish')
    )

    name = models.CharField(max_length = 255)
    description = models.TextField(blank=True, default="")
    status =  models.CharField(max_length = 25, choices = CHOICE_STATUS, default = 'draft')
    
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    slug = AutoSlugField(populate_from='name', unique=True)

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # TODO Add editor option
    # editor = models.ManyToMany(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    tags = TaggableManager()



    # TODO Add the logo img field

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    public = PublishedQuizManager()
    
    visited = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)


    def get_absolute_url(self):
        return reverse('trivia:quiz_detail',args=[self.pk])
    
    #def get_questions_url(self):
    #    return reverse('trivia:quiz',args=[self.pk])



class Question(models.Model):
    question = models.CharField(max_length = 255)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    @abc.abstractmethod
    def is_answer_correct(self, data):
        """Returns True if the answer is correct"""
        return
    
    def get_absolute_url(self):
        return reverse('trivia:question',args=[self.quiz.pk, self.pk])

    def __str__(self):
        return self.question

    def cast(self):
        """ Casts the object to get the original type

            Extracted from:
                - https://stackoverflow.com/questions/5225556/determining-django-model-instance-types-after-a-query-on-a-base-class
        """
        for name in dir(self):
            try:
                attr = getattr(self, name)
                if isinstance(attr, self.__class__):
                    return attr
            except:
                pass
        return self

class MultiChoiceQuestion(Question):
    
    CHOICE_TYPE = (
        ('single', 'Single Answer'),
        ('multi', 'Multiple Answers'),
    )

    qtype  = models.CharField(max_length = 25, choices = CHOICE_TYPE, default = 'single')

    def is_answer_correct(self, data):
        answers = MultiChoiceAnswer.objects.filter(question=self)
        if 'answer' not in data:
            return False
        answers = answers.filter(pk=int(data['answer'])).first()
        return answers.is_correct

class MultiChoiceAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length = 255, default="")
    is_correct = models.BooleanField(default=False)

class TextQuestion(Question):
    text_answer = models.TextField()

    def is_answer_correct(self, data):
        if 'answer' not in data:
            return False
        return data['answer']==self.text_answer





# TODO Solve this in a more elegant way
# I should add here the finished migration file with the corrected solution