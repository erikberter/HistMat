import random
import string

from .models import *

def tuple_find(tuple_pair, key):
    try:
        return dict(tuple_pair)[key]
    except:
        return None

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def contains_valid_string(string, dict):
    if string in dict:
        if dict.get(string):
            return True
    return False


def get_book_state(user, book):
    try:
        book_ud = BookUserDetail.objects.filter(book=book).get(user=user)
    except:
        return "None"
    state = BookUserDetail.BOOK_STATE_L.index(book_ud.book_state)
    return BookUserDetail.BOOK_STATE[state][1]

def is_book_in_user(user, book):
    return BookUserDetail.objects.filter(book=book).filter(user = user).count() > 0

def get_user_act_page(user, book):
    return BookUserDetail.objects.filter(book=book).distinct().filter(user = user).first().act_page