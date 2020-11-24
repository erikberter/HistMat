from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings

import abc
import uuid 

from simple_history.models import HistoricalRecords
from taggit.managers import TaggableManager
from autoslug import AutoSlugField

import json
from django.core.serializers.python import Serializer

from django.core.serializers.json import DjangoJSONEncoder

import logging

logger = logging.getLogger(__name__)



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

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('trivia:quiz_detail',args=[self.slug])
    
    


def questionSelect( questions):
    data = {}
    question_dict = []
    for question in questions:
        ret_data = question.cast().get_dict()
        question_dict.append(ret_data.copy())
    data["questions"] = question_dict
    
    print(data)
    return data

def get_question_type(question):
    for qtype in QUESTION_TYPES:
        if isinstance(question.cast(), qtype[0]):
            return qtype[1]
    return "none"

QUESTION_TYPES_TEXT = (
        ("multichoice", "Multichoice Question"),
        ("text" , "Text"),
        )
class Question(models.Model):
    question_type = models.CharField(max_length = 25, choices = QUESTION_TYPES_TEXT, default = 'text')
    question = models.CharField(max_length = 255)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    @abc.abstractmethod
    def is_answer_correct(self, data):
        """Returns True if the answer is correct"""
        return
    
    def get_dict(self):
        data = { "question" : self.question, "question_type" : get_question_type(self)}
        return data

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
        answers = answers.get(pk=int(data['answer']))
        return answers.is_correct

    def get_dict(self):
        data = super().get_dict()
        answers_list = []
        answers = MultiChoiceAnswer.objects.filter(question=self)
        for answer in answers:
            answers_list.append(answer.get_dict().copy())

        data["answers"] = answers_list

        return data

class MultiChoiceAnswer(models.Model):
    question = models.ForeignKey(Question, related_name="answers", on_delete=models.CASCADE)
    answer = models.CharField(max_length = 255, default="")
    is_correct = models.BooleanField(default=False)

    def get_dict(self):
        return {'answer' : self.answer, 'is_correct' : self.is_correct}

class TextQuestion(Question):
    answer = models.TextField()

    def is_answer_correct(self, data):
        if 'answer' not in data:
            return False
        return data['answer']==self.answer

    def get_dict(self):
        data = super().get_dict()
        data["answer"] = self.answer
        return data

# TODO Solve this in a more elegant way
# I should add here the finished migration file with the corrected solution

QUESTION_TYPES = (
        (MultiChoiceQuestion, "multichoice"),
        (TextQuestion , "text"),
        )
