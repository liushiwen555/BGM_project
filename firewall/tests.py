from django.test import TestCase
# Create your tests here.


from timeit import timeit
from io import StringIO


source = ['foo']*1000


def str_io():
    buf = StringIO()
    for i in source:
        buf.write(i)
    final = buf.getvalue()


def str_join():
    out = []
    for i in source:
        out.append(i)
    # final = ''.join(out)


def str_concat():
    out = ""
    for i in source:
        out += i


t = timeit('str_io()', 'from __main__ import str_io', number=10000)
print(t)

t = timeit('str_join()', 'from __main__ import str_join', number=10000)
print(t)
# 1000 loops, best of 3: 9.89 ms per loop


t = timeit('str_concat()', 'from __main__ import str_concat', number=10000)
print(t)
