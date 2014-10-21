from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    "",
    url(r"^response/$", views.ResponseView.as_view(),
        name="django_payzen_response"),
)
