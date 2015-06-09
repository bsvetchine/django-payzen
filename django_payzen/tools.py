"""Some tools."""

import hashlib
import logging
import random

from . import app_settings

logger = logging.getLogger(__name__)


def get_vads_trans_id(vads_site_id, vads_trans_date):
    """
    Returns a default value for vads_trans_id field.

    vads_trans_id field is mandatory. It is composed by 6 numeric
    characters that identifies the transaction. There is a unicity contraint
    between vads_site_id and vads_trans_date (the first 8 characters
    representing the transaction date).

    We consider the probability of having 2 identical
    generated vads_trans_id in the same day as null."""
    vads_trans_id = ""
    for i in range(0, 6):
        vads_trans_id += str(random.randint(0, 9))
    return vads_trans_id


def get_custom_payment_config(payments_conf):
    """
    Returns the payzen value for vads_payment_config for multi payments.

    If CustomPaymentConfig are set (m2m relationship), returns the payzen
    string for vads_payment_config.
    """
    conf = 'MULTI_EXT:'
    for pc in payments_conf:
        conf += str(pc) + ';'
    return conf[:-1]


def get_vads_payment_config(general_conf, custom_payments_conf):
    """
    Returns the vads_payment_config string respecting to payzen format.

    According to the foreignKey relationship to MultiPaymentConfig or the
    ManyToMany relationship to CustomPaymentConfig, returns the value
    for vads_payment_config.
    It should not be possible to edit at the same time a MultiPaymentConfig
    and a CustomPaymentConfig (does not make sense). It this case appends,
    the CustomPaymentConfig only is considered.
    """
    if custom_payments_conf:
        return get_custom_payment_config(custom_payments_conf)
    if general_conf:
        return str(general_conf)
    return 'SINGLE'


def get_signature(payment_request):
    """
    Returns the signature for the transaction.

    To compute the signature, first you have to get the value of all
    the fields that starts by 'vads_', ordering them alphabetically.
    All the values are separated by the '+' character. Then you add
    the value of the payzen certificate.
    Finaly you hash the string using sha1."""

    vads_args = {}
    for field in payment_request._meta.fields:
        if field.name[:5] == 'vads_':
            field_value = field.value_from_object(payment_request)
            if field_value:
                vads_args.update({
                    field.name: field_value
                })
    base_str = ''
    for key in sorted(vads_args):
        base_str += str(vads_args[key]) + '+'
    base_str += app_settings.VADS_CERTIFICATE
    return hashlib.sha1(base_str.encode("utf-8")).hexdigest()


def is_signature_valid(post_args):
    vads_args = [arg for arg in post_args if arg.startswith("vads_")]
    signature_str = ""
    for key in sorted(vads_args):
        signature_str += post_args[key] + "+"
    signature_str += app_settings.VADS_CERTIFICATE
    return post_args.get("signature") and (hashlib.sha1(
        signature_str.encode("utf-8")).hexdigest() == post_args["signature"])


def process_response(data):
    """Process a payment response."""
    # We check if the signature is valid. If not return
    if not is_signature_valid(data):
        logger.warning(
            "Django-Payzen : Response signature detected as invalid",
            extra={"stack": True}
        )
        return None

    from . import forms
    from . import models

    # The signature is valid
    vads_trans_id = data.get("vads_trans_id")
    vads_trans_date = data.get("vads_trans_date")
    vads_site_id = data.get("vads_site_id")
    try:
        instance = models.PaymentResponse.objects.get(
            vads_trans_id=vads_trans_id,
            vads_trans_date=vads_trans_date,
            vads_site_id=vads_site_id)
        form = forms.PaymentResponseForm(data, instance=instance)
    except models.PaymentResponse.DoesNotExist:
        form = forms.PaymentResponseForm(data)
    if form.is_valid():
        response = form.save()
        logger.info("Django-Payzen : Transaction {} response received !"
                    .format(response.vads_trans_id))
    else:
        logger.error("Django-Payzen : Response could not be saved - {} {}"
                     .format(form.errors, data),
                     extra={"stack": True})
        response = None
    return response
