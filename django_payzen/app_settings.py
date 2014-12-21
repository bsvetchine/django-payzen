""" Default payzen settings.

All settings should be set in the django settings file and not
directly in this file.
We deliberately do not set up default values here in order to
force user to setup explicitely the default behaviour."""

from django.conf import settings


PAYZEN_REQUEST_URL = 'https://secure.payzen.eu/vads-payment/'
VADS_CONTRIB = 'django-payzen v1.0'
VADS_SITE_ID = getattr(settings, 'VADS_SITE_ID')
VADS_CERTIFICATE = getattr(settings, 'VADS_CERTIFICATE')
VADS_CTX_MODE = getattr(settings, 'VADS_CTX_MODE')
VADS_CURRENCY = getattr(settings, 'VADS_CURRENCY', None)
VADS_ACTION_MODE = getattr(settings, 'VADS_ACTION_MODE', None)
