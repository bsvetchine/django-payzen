PaymentRequest
==============

Have a look at the `Payment Request model <https://github.com/bsvetchine/django-payzen/blob/master/django_payzen/models.py>`_ and at the `Payzen documentation <https://www.payzen.eu/wp-content/uploads/integration/Guide_d_implementation_formulaire_paiement_V2_Payzen_V2.9f.pdf>`_ to see all the parameters that are supported by payzen.

Be careful about the amount parameter ; its value is always a positive integer repesenting the amount in cents.

::

    from django_payzen import models as pz_models

    payment_request = pz_models.PaymentRequest(
        amount=1000  # corresponds to 10 € if no vads_currency supplied
    )
    payment_request.save()

    payment_request = pz_models.PaymentRequest(
        amount=1000,
        vads_url_success='http://www.loadingdata-band.com/',
        vads_url_refused='http://www.loadingdata-band.com/',
        vads_url_cancel='http://www.loadingdata-band.com/',
        order_id=1,
        order_info="Loading Data c'est d'la boulette",
        order_info2="puis Blues Pills aussi",
        vads_trans_id="000001"
    )
    payment_request.save()


1.1 Special PaymentRequest fields

.. _models_PaymentRequest_vads_trans_id

``vads_trans_id``
---------------------

vads_trans_id is a value composed by 6 numeric characters representing the id of the transaction. There is a unicity constraint betweend vads_trans_date and vads_site_id.
vads_trans_id field is mandatory. If not set by user, django-payzen will generate randomly its value, considering the probability of having 2 generated values identical for the same day as null.


The following fields should not be set manually. Their value are computed during the save() or update() methods. Their value are computed from all other parmeters. Thus, there are some precations to take :

 * if you create PaymentRequest objects using django model create function or in bulk_create, do not forget to call PaymentRequest update() method to compute the following fields.
 * if you update parameters relative to the payment (could be PaymentRequest fields or adding a CustomPaymentConfig object to the PaymentRequest object, do not forget to call the update() method to update all computed fields.

.. _models_PaymentRequest_signature

``signature``
-------------

signature field is security parameter sent to payzen with all other payment data. The signature is computed from payment request parameters and hashed using sha1.

.. _models_PaymentRequest_vads_payment_config

``vads_payment_config``
---------------------

vads_payment_config is a string parameter allowing to set up a multiple payments.
To set up multiple payments that you have 2 possibilities :
 * edit a MultiPaymentConfig object. This is the simplest method hower not highly customizable.
 * add one or several CustomPaymentConfig objects. This allows you to select the payment date and amount for every payment process.

.. _models_PaymentRequest_vads_theme_config

``vads_theme_config``
---------------------

vads_theme_config is a string parameter allowing to customize payzen payment pages. vads_theme_config string is computed from the ThemeConfig object linked. If no ThemeConfig is set, vads_theme_config is null.
