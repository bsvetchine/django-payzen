Installation
============

1. Install django-payzen package.

::

    pip install django-payzen


2. Add django_payzen in your INSTALLED_APPS

Edit your django settings.py and add django_payzen in your INSTALLED_APPS.

2. Configure your :doc:`django-payzen settings </settings>` .

In your settings.py file, add the settings specific to django-payzen.

3. Include "django_payzen.urls" in your urls.py

::

    url(r'^payment/', include("django_payzen.urls")),
