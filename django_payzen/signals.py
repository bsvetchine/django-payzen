"""django-payzen signals."""
import django.dispatch

response_error = django.dispatch.Signal()
payment_success = django.dispatch.Signal(providing_args=["response"])
payment_failure = django.dispatch.Signal(providing_args=["response"])
