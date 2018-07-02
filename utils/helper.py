import string
import random


def random_string(str_length):
    base_str = string.ascii_letters + string.digits
    random_str = ''
    length = len(base_str) - 1
    for i in range(str_length):
        random_str += base_str[random.randint(0, length)]
    return random_str
