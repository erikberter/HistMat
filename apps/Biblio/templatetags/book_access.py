from django import template
from apps.Biblio.models import *
from django.shortcuts import  get_object_or_404
from django.db.models import Q

register = template.Library()

@register.simple_tag
def get_book_state(user, book):
    try:
        book_ud = BookUserDetail.objects.filter(book=book).get(user=user)
    except:
        return "None"
    state = BookUserDetail.BOOK_STATE_L.index(book_ud.book_state)
    return BookUserDetail.BOOK_STATE[state][1]

@register.simple_tag
def is_book_in_user(user, book):
    try:
        book_ud_c = BookUserDetail.objects.filter(
            Q(book=book) & Q(user = user) 
            ).count()
    except:
        return False
    return book_ud_c > 0

@register.simple_tag
def is_book_act_page_in_user(user, book):
    
    try:
        book_ud_c = BookUserDetail.objects.get(
            Q(book=book) & Q(user = user) 
            ).act_page
    except:
        book_ud_c = 0
    
    
    return book_ud_c 