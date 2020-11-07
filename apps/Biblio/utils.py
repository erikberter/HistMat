import random
import string

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
