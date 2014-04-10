from datetime import datetime

from django.db import models


class Order(models.Model):
    created = models.DateTimeField(default=datetime.now)


class Job(models.Model):
    order = models.ForeignKey(Order)
    lang = models.TextField()
    source = models.TextField()
    translation = models.TextField()
    status = models.TextField()
