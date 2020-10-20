from django import template
from apps.Biblio.models import *
from django.shortcuts import  get_object_or_404
from django.db.models import Q

register = template.Library()

@register.simple_tag
def get_book_state(user, book):
    
    book_ud = BookUserDetail.objects.filter(
                 Q(book=book) & Q(user = user) 
            ).first() 
    
    state = BookUserDetail.BOOK_STATE_L.index(book_ud.book_state)
    return BookUserDetail.BOOK_STATE[state][1]

@register.simple_tag
def is_book_in_user(user, book):
    
    book_ud_c = BookUserDetail.objects.filter(
                 Q(book=book) & Q(user = user) 
            ).count()
    
    return book_ud_c>0