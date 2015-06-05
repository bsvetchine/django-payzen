"""Django-Payzen views."""

from django import http
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from . import signals
from . import tools


class ResponseView(generic.View):

    http_method_names = [u'post']

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        response = tools.process_response(request.POST)
        if response:
            if response.payment_successful:
                signal = signals.payment_success
            else:
                signal = signals.payment_failure
            signal.send(sender=self.__class__, response=response)
        else:
            signals.response_error.send(sender=self.__class__)
        return http.HttpResponse()
