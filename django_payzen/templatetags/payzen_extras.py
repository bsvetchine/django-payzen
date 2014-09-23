from django import template

from .. import app_settings
from .. import forms

register = template.base.Library()


@register.simple_tag
def payzen_form(payment_request):
    """TODO docstring."""
    payment_request.update()
    t = template.loader.get_template("django_payzen/form.html")
    return t.render(template.Context({
        "form": forms.PaymentRequestForm(instance=payment_request),
        "payzen_submit_url": app_settings.PAYZEN_REQUEST_URL
    }))
