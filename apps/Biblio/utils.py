

def tuple_find(tuple_pair, key):
    res = [y for (x, y) in tuple_pair if x == key]
    if res:
        return res[0]
    else:
        return None