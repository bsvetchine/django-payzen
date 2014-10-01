Settings
========

.. _settings_vads_site_id

``VADS_SITE_ID``
----------------

Mandatory setting : your payzen client ID. You will find it in `your payzen dashboard <https://secure.payzen.eu/vads-merchant/>`_ .

.. _settings_vads_certificate

``VADS_CERTIFICATE``
--------------------

Mandatory setting : the payzen certificate to use. You can generate a certificate in your payzen dashboard. There are 2 certificates ; one for testing purposes and one for production.

.. _settings_vads_ctx_mode

``VADS_CTX_MODE``
-----------------

Mandatory setting : 'TEST' or 'PRODUCTION'. Remark : be careful to set the VADS_CERTIFICATE value accordingly to the VADS_CTX_MODE.

.. _settings_vads_currency

``VADS_CURRENCY``
-----------------

Default currency used if the currency is not explicitely set in the payment request. vads_currency value should be the ISO 4217 code of the currency. By default vads_currency = 978, which corresponds to €.
You can have look at the django_payzen.constants.VADS_CURRENCY_CHOICES variable to see the supported currencies.

.. _settings_vads_action_mode

``VADS_ACTION_MODE``
--------------------

Default vads_action_mode used in the payment request. vads_action_mode can be set to :
'INTERACTIVE' : if the card information retrieval is done by payzen (default).
'SILENT' : if all card information retrieval is done by merchant site.

