from django.db import models
from polymorphic.models import PolymorphicModel
import abc


class Quiz(models.Model):
    name = models.CharField(max_length = 255)

class Question(models.Model):
    question = models.CharField(max_length = 255)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    @abc.abstractmethod
    def is_answer_correct(self, data):
        """Method documentation"""
        return
    
    def __str__(self):
        return str(self.pk)

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