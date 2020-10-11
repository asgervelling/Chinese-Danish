from string import ascii_lowercase
from random import choice

def any_is_empty(*strings:str):
    for i in strings:
        if len(i) < 2:
            return True
    return False

def random_word(length):
    letters = ascii_lowercase
    return ''.join(choice(letters) for i in range(length))