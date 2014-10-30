import logging

from django import http
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from . import forms
from . import models
from . import signals
from . import tools

logger = logging.getLogger(__name__)


class ResponseView(generic.View):

    http_method_names = [u'post']

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        # We check if the signature is valid. If not return
        if not tools.is_signature_valid(request.POST):
            logger.warning(
                "Django-Payzen : Response signature detected as invalid",
                extra={"stack": True})
            return http.HttpResponse()
        # Payzen data is checked and valid
        form = forms.PaymentResponseForm(request.POST)
        if form.is_valid():
            try:
                vads_trans_id = form.cleaned_data.get("vads_trans_id")
                vads_trans_date = form.cleaned_data.get("vads_trans_date")
                vads_site_id = form.cleaned_data.get("vads_site_id")
                instance = models.PaymentResponse.objects.get(
                    vads_trans_id=vads_trans_id,
                    vads_trans_date=vads_trans_date,
                    vads_site_id=vads_site_id)
                response = form.save(instance=instance)
            except models.PaymentResponse.DoesNotExist:
                response = form.save()
            logger.info("Django-Payzen : Transaction {} response received !"
                        .format(response.vads_trans_id))
            if response.payment_successful:
                signal = signals.payment_success
            else:
                signal = signals.payment_failure
            signal.send(sender=self.__class__, response=response)
        else:
            logger.error("Django-Payzen : Response could not be saved - {}"
                         .format(form.errors), extra={"stack": True})
            signals.response_error.send(sender=self.__class__)
        return http.HttpResponse()
