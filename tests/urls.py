"""base urls.py for testing purpose."""

from django.conf.urls import include, url


urlpatterns = [
    url(r"payment/", include("django_payzen.urls")),
]
