Signals
=======

You may need to automate actions once a payment is received or rejected or if django_payzen cannot read/analyze payzen responses. The following signals allow you to do that.

.. _signals_payment_success

``payment_success``
-------------------

signal sent once a payment sucessful response is received and saved. The PaymentResponse object is sent in argument.

.. _signals_payment_failure

``payment_failure``
-------------------

signal sent once a payment unsuccessful response is received and saved. You can analyze data in PaymentResponse to check what wend wrong. The PaymentResponse object is sent in argument.

.. _signals_payment_error

``payment_error``
-------------------

signal sent if django_payzen cannot read or analyze the request sent by payzen.
