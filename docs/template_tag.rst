template_tag
============

Once you have a PaymentRequest object, you can proceed with the payment following theses steps :

1. Set up a django view that provide the PaymentRequest object to a template

2. In this template, load payzen template tags and call payzen_form tag

::

    {% load payzen_extras %}

    {% payzen_form object %}


payzen_form tag renders a hidden form including all PaymentRequest data. The form is directly submitted to payzen url and the user is redirected to payzen card registration process.

By default payzen_form will not autosubmit itself. You can do that calling :

::

    {% payzen_form object auto_submit=True %}
