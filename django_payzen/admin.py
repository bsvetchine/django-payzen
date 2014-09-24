from django.contrib import admin

from . import models


class PaymentRequestAdmin(admin.ModelAdmin):
    model = models.PaymentRequest
    list_display = ("vads_amount", "get_vads_currency_display",
                    "vads_trans_id", "vads_trans_date")


class PaymentResponseAdmin(admin.ModelAdmin):
    model = models.PaymentResponse
    list_display = ("vads_amount", "get_vads_currency_display",
                    "vads_trans_id", "vads_trans_date",
                    "vads_operation_type")


admin.site.register(models.PaymentRequest, PaymentRequestAdmin)
admin.site.register(models.PaymentResponse, PaymentResponseAdmin)
