import logging

from django import http
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from . import forms
from . import signals

logger = logging.getLogger(__name__)


class ResponseView(generic.View):

    http_method_names = [u'post']

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        filtered_data = {}
        for key, value in request.POST.items():
            if value:
                if (isinstance(value, list) and len(value)):
                    filtered_data.update({key: value[0]})
                else:
                    filtered_data.update({key: value})
        form = forms.PaymentResponseForm(filtered_data)
        if form.is_valid():
            response = form.save()
            logger.info("Django-Payzen : Transaction {} response received !"
                        .format(response.vads_trans_id))
            if response.payment_successful:
                signal = signals.payment_success
            else:
                signal = signals.payment_failure
            signal.send(
                sender=self.__class__,
                response=response)
        else:
            logger.error("Django-Payzen : Response could not be saved - {}"
                         .format(form.errors))
            signals.response_error.send(sender=self.__class__)
        return http.HttpResponse()
