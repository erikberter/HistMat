from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

import abc

from django.conf import settings


class Quiz(models.Model):

    CHOICE_STATUS = (
        ('draft', 'Draft'),
        ('publish', 'Publish')
    )

    name = models.CharField(max_length = 255)
    status =  models.CharField(max_length = 25, choices = CHOICE_STATUS, default = 'draft')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('trivia:quiz_detail',args=[self.pk])
    
    def get_questions_url(self):
        return reverse('trivia:quiz',args=[self.pk])



class Question(models.Model):
    question = models.CharField(max_length = 255)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    @abc.abstractmethod
    def is_answer_correct(self, data):
        """Method documentation"""
        return
    
    def get_absolute_url(self):
        return reverse('trivia:question',args=[self.quiz.pk, self.pk])

    def __str__(self):
        return self.question

    #https://stackoverflow.com/questions/5225556/determining-django-model-instance-types-after-a-query-on-a-base-class
    def cast(self):
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