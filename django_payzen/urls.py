from django.conf.urls import  url

from . import views

urlpatterns = [
    url(r"^response/$", views.ResponseView.as_view(),
        name="django_payzen_response"),
]
