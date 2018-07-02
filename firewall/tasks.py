from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@shared_task
def add(x, y):
    logger.info(x+y)
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task()
def test(arg):
    print(arg)
