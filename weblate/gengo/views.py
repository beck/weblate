"""Gengo views."""
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.views.generic.edit import FormMixin
from django.template import RequestContext
from django.template.loader import render_to_string

from weblate.trans.models import Unit

from weblate.gengo import api


class GengoUI(object):

    """HTML generator for the translation edit view."""

    def __init__(self, **kwargs):
        """Accept a unit and request (request required for csrf)."""
        self.request = kwargs.get('request')
        self.unit = kwargs.get('unit')

    def html(self):
        """Return UI for the gengo API."""
        context = {'unit': self.unit}
        context_instance = RequestContext(self.request)
        return render_to_string('gengo/ui.html', context, context_instance)


class Order(View, FormMixin):

    """View for ordering translation from gengo."""

    def post(self, request):
        """Take a weblate unit and create a gengo order."""
        pk = self.get_form_kwargs()['data']['unit']
        unit = Unit.objects.get(pk=pk)
        job = {
            'body_src': unit.source,
            'comment': 'Hello World',
            'lc_src': 'en',
            'lc_tgt': unit.translation.language.code,
            'tier': 'standard',
            'purpose': 'Web localization',
        }
        api.post_jobs([job])
        url = request.META['HTTP_REFERER']
        return HttpResponseRedirect(url)
