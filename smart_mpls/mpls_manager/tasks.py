# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task
from demoapp.models import Widget


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
def count_widgets():
    return Widget.objects.count()
