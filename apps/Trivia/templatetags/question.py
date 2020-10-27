from django import template
from apps.Biblio.models import *
from django.shortcuts import  get_object_or_404
from django.db.models import Q

register = template.Library()

@register.simple_tag
def is_answer_correct(question, answer):
    return question.is_answer_correct({'answer':answer})