# from __future__ import absolute_import
# import os
# from celery import Celery
# from django.conf import settings
# from celery.schedules import crontab
#
# # set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ssms.settings')
# app = Celery('ssms')
#
# # Using a string here means the worker will not have to
# # pickle the object when using Windows.
# app.config_from_object('django.conf:settings')
#
# # app.conf.beat_schedule = {
# #     'test_schedule': {
# #         'task': 'items.tasks.send_schedule_mail',
# #         'schedule': crontab(hour=9, minute=49, day_of_week='*'),
# #         'args': (16,)
# #     },
# # }
#
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
#
#
# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))
