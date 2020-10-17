# from __future__ import absolute_import
# from celery import shared_task
# from django.core.mail import send_mail
# from celery.utils.log import get_task_logger
# import time
# loger = get_task_logger(__name__)
#
#
# @shared_task()
# def send_task_mail(mailbody, email_address):
#     time.sleep(10)
#     send_mail("New Order", mailbody, "SSMS Admin", [email_address])
#     loger.info('Mail sent to "%s" ' % email_address)
#     return
#
#
# @shared_task()
# def send_schedule_mail(email_address):
#     loger.info('Mail sent to "%s" ' % email_address)
#     return
