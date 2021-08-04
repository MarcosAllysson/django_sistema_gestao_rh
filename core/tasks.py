# Create your tasks here

from celery import shared_task
# from demoapp.models import Widget
from django.core.mail import send_mail


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task
def send_relatorio():
    send_mail(
        'Relatório celery',
        'Relatório processado com celery',
        'django@gmail.com',
        ['contatodjango@gmail.com'],
        fail_silently=False
    )

    return True


# @shared_task
# def count_widgets():
#     return Widget.objects.count()
#
#
# @shared_task
# def rename_widget(widget_id, name):
#     w = Widget.objects.get(id=widget_id)
#     w.name = name
#     w.save()