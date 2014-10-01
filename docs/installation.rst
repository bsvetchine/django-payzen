Installation
============

1. Install django-payzen package.

::

    pip install https://github.com/bsvetchine/django-payzen/archive/master.zip


2. Configure django-payzen settings :doc:`/settings`.


3. Include "django_payzen.urls" in your urls.py

::

    url(r'^payment/', include("django_payzen.urls")),
