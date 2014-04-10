"""Gengo app urls."""
from django.conf.urls import patterns, url

from weblate.gengo.views import Order

urlpatterns = patterns(
    '',
    url(r'^order/', Order.as_view(), name='order'),
)
