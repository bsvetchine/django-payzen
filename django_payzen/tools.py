import hashlib

from . import app_settings


def get_vads_trans_id(vads_site_id, vads_trans_date):
    """
    Returns a default value for vads_trans_id field.

    vads_trans_id field is mandatory. It is composed by 6 alphanumeric
    characters that identifies the transaction. There is a unicity contraint
    between vads_site_id and vads_trans_date (the first 8 characters
    representing the transaction date).

    This function returns '000001' for the first transaction of
    the day, and then increments it."""

    from . import models  # Avoid circular imports

    counter = models.PaymentRequest.objects.filter(
        vads_site_id=vads_site_id,
        vads_trans_date__startswith=vads_trans_date[:8]).count()
    vads_trans_id = str(counter+1)
    while len(vads_trans_id) < 6:
        vads_trans_id = '0' + vads_trans_id
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
    base_str += app_settings.CLIENT_CERTIFICATE
    return hashlib.sha1(base_str).hexdigest()