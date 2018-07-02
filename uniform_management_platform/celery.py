from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.utils.log import get_task_logger
from celery.schedules import crontab


logger = get_task_logger(__name__)
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniform_management_platform.settings')

app = Celery('uniform_management_platform')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 5 seconds.
#     sender.add_periodic_task(30.0, aaa.s(), name='add every 10')
#
#     # # Calls test('world') every 30 seconds
#     # sender.add_periodic_task(30.0, test.s(), expires=10)
#     #
#     # # Executes every Monday morning at 7:30 a.m.
#     # sender.add_periodic_task(
#     #     crontab(hour=7, minute=30, day_of_week=1),
#     #     test.s('Happy Mondays!'),
#     # )
#
#
# @app.task()
# def aaa():
#     print('Hello world')
