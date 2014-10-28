"""
Models for Payzen - Payment using webform v2

The models are implemented according to the document :
'Guide_d_implementation_formulaire_paiement_V2_Payzen_v2.9f.pdf'

TODO add validators to manage payzen contraints on special fields.
"""

import datetime

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import utc

from . import app_settings
from . import tools
from . import constants


auth_user_model = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


@python_2_unicode_compatible
class ThemeConfig(models.Model):
    """Model that contains the theme parameters of the payment form.

    To set up a theme is optional.
    """
    success_footer_msg_return = models.TextField(blank=True, null=True)
    cancel_footer_msg_return = models.TextField(blank=True, null=True)
    secure_message = models.TextField(blank=True, null=True)
    secure_message_register = models.TextField(blank=True, null=True)
    site_id_label = models.TextField(blank=True, null=True)
    css_for_payment = models.URLField(blank=True, null=True)
    css_for_payment_mobile = models.URLField(blank=True, null=True)
    header_for_mail = models.URLField(blank=True, null=True)
    footer_for_mail = models.URLField(blank=True, null=True)
    shop_logo = models.URLField(blank=True, null=True)

    def __str__(self):
        vads_theme_config = ""
        for field in self._meta.fields:
            if not field.auto_created:
                vads_theme_config += "{}={};".format(
                    field.name.upper(), field.value_from_object(self))
        return vads_theme_config[:-1]


@python_2_unicode_compatible
class MultiPaymentConfig(models.Model):
    """Model that contains parameters for multi-payment.

    Model fields:
    first -- the amount of the first payment.
    count -- the number of payments.
    period -- the number of days between two payments.

    Exemple:
    If you setup vads_amount to 10000 and a MultiPaymentConfig with
    first=5000, count=3, period=2, a first payment of 5000  will take place
    in 2 days from now, then a 2nd payment of 2500 will append 2 days after
    the first payment and a third payment of 2500 2 days later.
    """
    first = models.PositiveIntegerField()
    count = models.PositiveIntegerField()
    period = models.PositiveIntegerField()

    def __str__(self):
        return "MULTI:first={};count={};period={}".format(
            self.first, self.count, self.period)


@python_2_unicode_compatible
class CustomPaymentConfig(models.Model):
    """Model to manage a custom payment scheduler."""
    date = models.DateField()
    amount = models.PositiveIntegerField()

    def __str__(self):
        return "{}={}".format(
            self.date.strftime("%Y%m%d"), self.amount)


@python_2_unicode_compatible
class VADContract(models.Model):
    """Model to manage several VAD contrats.

    This model is useful when you have several VAD contracts and
    you want to dynamically change the VAD contract used."""
    cb_contract_num = models.CharField(max_length=32)
    amex_contract_num = models.CharField(max_length=32)

    def __str__(self):
        return "vads_contracts=CB={};AMEX={}".format(
            self.cb_contract_num, self.amex_contract_num)


class CustomerDetails(models.Model):
    """Abstract model that contains all data relative to the customer."""

    vads_cust_address = models.CharField(
        max_length=255, blank=True, null=True)
    vads_cust_address_number = models.CharField(
        max_length=5, blank=True, null=True)
    vads_cust_country = models.CharField(
        max_length=2, blank=True, null=True)
    vads_cust_email = models.EmailField(
        blank=True, null=True)
    vads_cust_id = models.CharField(
        max_length=63, blank=True, null=True)
    vads_cust_name = models.CharField(
        max_length=127, blank=True, null=True)
    vads_cust_last_name = models.CharField(
        max_length=63, blank=True, null=True)
    vads_cust_first_name = models.CharField(
        max_length=63, blank=True, null=True)
    vads_cust_cell_phone = models.CharField(
        max_length=32, blank=True, null=True)
    vads_cust_phone = models.CharField(
        max_length=32, blank=True, null=True)
    vads_cust_title = models.CharField(
        max_length=63, blank=True, null=True)
    vads_cust_city = models.CharField(
        max_length=63, blank=True, null=True)
    vads_cust_status = models.CharField(
        max_length=63, blank=True, null=True)
    vads_cust_state = models.CharField(
        max_length=63, blank=True, null=True)
    vads_cust_zip = models.CharField(
        max_length=63, blank=True, null=True)
    vads_language = models.CharField(
        max_length=2, blank=True, null=True)

    class Meta:
        abstract = True


class OrderDetails(models.Model):
    """Abstract model that contains all data relative to the order."""

    vads_order_id = models.CharField(
        max_length=32, blank=True, null=True)
    vads_order_info = models.CharField(
        max_length=255, blank=True, null=True)
    vads_order_info2 = models.CharField(
        max_length=255, blank=True, null=True)
    vads_order_info3 = models.CharField(
        max_length=255, blank=True, null=True)

    class Meta:
        abstract = True


class ShippingDetails(models.Model):
    """Abstract model that contains all data relative to shipping."""

    vads_ship_to_name = models.CharField(
        max_length=127, blank=True, null=True)
    vads_ship_to_first_name = models.CharField(
        max_length=63, blank=True, null=True)
    vads_ship_to_last_name = models.CharField(
        max_length=63, blank=True, null=True)
    vads_ship_to_street_number = models.CharField(
        max_length=5, blank=True, null=True)
    vads_ship_to_street = models.CharField(
        max_length=255, blank=True, null=True)
    vads_ship_to_street2 = models.CharField(
        max_length=255, blank=True, null=True)
    vads_ship_to_zip = models.CharField(
        max_length=63, blank=True, null=True)
    vads_ship_to_city = models.CharField(
        max_length=63, blank=True, null=True)
    vads_ship_to_country = models.CharField(
        max_length=2, blank=True, null=True)
    vads_ship_to_phone_num = models.CharField(
        max_length=32, blank=True, null=True)
    vads_ship_to_state = models.CharField(
        max_length=255, blank=True, null=True)

    class Meta:
        abstract = True


class RequestDetails(models.Model):
    """Abstract model that contains all data relative to transaction."""

    vads_action_mode = models.CharField(
        max_length=11, choices=constants.VADS_ACTION_MODE_CHOICES,
        default=app_settings.VADS_ACTION_MODE)
    vads_amount = models.PositiveIntegerField()
    vads_currency = models.CharField(
        max_length=3, choices=constants.VADS_CURRENCY_CHOICES,
        default=app_settings.VADS_CURRENCY)
    vads_ctx_mode = models.CharField(
        max_length=10, choices=constants.VADS_CTX_MODE_CHOICES,
        default=app_settings.VADS_CTX_MODE)
    vads_page_action = models.CharField(
        max_length=7, default='PAYMENT')
    vads_payment_config = models.TextField()
    vads_site_id = models.PositiveIntegerField(
        default=app_settings.VADS_SITE_ID)
    vads_trans_date = models.CharField(
        max_length=14)
    vads_trans_id = models.CharField(max_length=6)
    vads_version = models.CharField(
        max_length=2, default='V2')
    signature = models.CharField(
        max_length=40)

    class Meta:
        abstract = True


class WarrantyDetails(models.Model):

    vads_threeds_enrolled = models.CharField(
        max_length=1, choices=constants.VADS_THREEDS_ENROLLED,
        blank=True, null=True)
    vads_threeds_cavv = models.CharField(max_length=28, blank=True, null=True)
    vads_threeds_eci = models.CharField(max_length=2, blank=True, null=True)
    vads_threeds_xid = models.CharField(max_length=28, blank=True, null=True)
    vads_threeds_cavvAlgorithm = models.CharField(
        choices=constants.VADS_THREEDS_CAVVALGORITHM_CHOICES,
        max_length=1, blank=True, null=True)
    vads_threeds_status = models.CharField(
        choices=constants.VADS_THREEDS_STATUS_CHOICES,
        max_length=1, blank=True, null=True)
    vads_threeds_sign_valid = models.NullBooleanField()
    vads_threeds_error_code = models.CharField(
        max_length=2, blank=True, null=True)
    vads_threeds_exit_status = models.CharField(
        max_length=2, blank=True, null=True)
    vads_warranty_result = models.CharField(
        max_length=13, blank=True, null=True)

    class Meta:
        abstract = True


class RiskControlDetail(models.Model):

    vads_extra_result = models.CharField(max_length=2, blank=True, null=True)
    vads_card_country = models.CharField(max_length=2, blank=True, null=True)
    vads_bank_code = models.CharField(max_length=2, blank=True, null=True)
    vads_bank_product = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        abstract = True


class CustomizationDetails(models.Model):

    vads_available_languages = models.TextField(blank=True, null=True)
    vads_theme_config = models.CharField(max_length=255, blank=True, null=True)
    vads_shop_url = models.URLField(blank=True, null=True)
    vads_shop_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        abstract = True


class PaymentResponse(WarrantyDetails, CustomerDetails,
                      OrderDetails, ShippingDetails,
                      CustomizationDetails):

    """Model that contains the main response parameters from Payzen."""

    signature = models.CharField(max_length=40)
    vads_ctx_mode = models.CharField(
        max_length=10, choices=constants.VADS_CTX_MODE_CHOICES)
    vads_url_check_src = models.CharField(
        choices=constants.VADS_URL_CHECK_SRC_CHOICES,
        max_length=10, blank=True, null=True)
    vads_version = models.CharField(max_length=2)
    vads_trans_date = models.CharField(max_length=14)
    vads_action_mode = models.CharField(
        max_length=11, choices=constants.VADS_ACTION_MODE_CHOICES,
        blank=True, null=True)

    vads_trans_id = models.CharField(max_length=6)
    vads_payment_config = models.TextField(
        blank=True, null=True)
    vads_sequence_number = models.PositiveSmallIntegerField(
        blank=True, null=True)
    vads_site_id = models.PositiveIntegerField()
    vads_amount = models.PositiveIntegerField(
        blank=True, null=True)
    vads_currency = models.CharField(
        max_length=3, choices=constants.VADS_CURRENCY_CHOICES,
        blank=True, null=True)
    vads_effective_amount = models.PositiveIntegerField(
        blank=True, null=True)
    vads_operation_type = models.CharField(
        max_length=6, choices=constants.VADS_OPERATION_TYPE_CHOICES,
        blank=True, null=True)
    vads_result = models.CharField(
        max_length=2, choices=constants.VADS_RESULT_CHOICES)
    vads_validation_mode = models.CharField(
        choices=constants.VADS_VALIDATION_MODE_CHOICES,
        max_length=1, blank=True, null=True)
    vads_trans_status = models.CharField(
        choices=constants.VADS_TRANS_STATUS, max_length=33)
    vads_effective_creation_date = models.CharField(
        max_length=14, blank=True, null=True)
    vads_presentation_date = models.CharField(
        max_length=14, blank=True, null=True)
    vads_capture_delay = models.PositiveIntegerField(blank=True, null=True)
    vads_card_brand = models.CharField(max_length=50, blank=True, null=True)
    vads_card_number = models.CharField(max_length=16, blank=True, null=True)
    vads_expiry_month = models.PositiveSmallIntegerField(blank=True, null=True)
    vads_expiry_year = models.PositiveSmallIntegerField(blank=True, null=True)
    vads_contract_used = models.CharField(
        max_length=250, blank=True, null=True)
    vads_auth_number = models.CharField(max_length=6, blank=True, null=True)
    vads_auth_result = models.CharField(max_length=2, blank=True, null=True)
    vads_auth_mode = models.CharField(
        max_length=4, choices=constants.VADS_AUTH_MODE_CHOICES,
        blank=True, null=True)
    vads_payment_certificate = models.CharField(
        max_length=40, blank=True, null=True)
    vads_payment_src = models.CharField(
        max_length=5, blank=True, null=True,
        choices=constants.VADS_PAYMENT_SRC_CHOICES)
    vads_contrib = models.CharField(
        max_length=255, blank=True, null=True)
    vads_user_info = models.CharField(max_length=255, blank=True, null=True)
    vads_ext_trans_id = models.CharField(
        max_length=6, blank=True, null=True)
    vads_payment_option_code = models.TextField(blank=True, null=True)

    vads_change_rate = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Response"
        unique_together = ("vads_trans_id", "vads_site_id", "vads_trans_date")

    @property
    def payment_successful(self):
        if self.vads_result == '00':
            return True
        return False

    @property
    def request(self):
        return PaymentRequest.objects.get(
            vads_trans_id=self.vads_trans_id,
            vads_trans_date=self.vads_trans_date,
            vads_site_id=self.vads_site_id)

    @property
    def user(self):
        try:
            return self.request.user
        except AttributeError:
            return None


class PaymentRequest(RequestDetails, CustomerDetails,
                     OrderDetails, ShippingDetails):
    """Model that contains all Payzen parameters to initiate a payment."""

    user = models.ForeignKey(auth_user_model, blank=True, null=True)

    vads_capture_delay = models.PositiveIntegerField(blank=True, null=True)
    vads_contrib = models.CharField(
        max_length=255, blank=True, null=True,
        default=app_settings.VADS_CONTRIB)
    vads_payment_cards = models.CharField(
        max_length=127, blank=True, null=True)
    vads_return_mode = models.CharField(
        max_length=12, choices=constants.VADS_RETURN_MODE_CHOICES,
        blank=True, null=True)
    vads_theme_config = models.CharField(
        max_length=255, blank=True, null=True)
    vads_validation_mode = models.CharField(
        choices=constants.VADS_VALIDATION_MODE_CHOICES,
        max_length=1, blank=True, null=True)
    vads_url_success = models.URLField(blank=True, null=True)
    vads_url_referral = models.URLField(blank=True, null=True)
    vads_url_refused = models.URLField(blank=True, null=True)
    vads_url_cancel = models.URLField(blank=True, null=True)
    vads_url_error = models.URLField(blank=True, null=True)
    vads_url_return = models.URLField(blank=True, null=True)
    vads_user_info = models.CharField(max_length=255, blank=True, null=True)
    vads_shop_name = models.CharField(max_length=255, blank=True, null=True)
    vads_redirect_success_timeout = models.PositiveIntegerField(
        blank=True, null=True)
    vads_redirect_success_message = models.CharField(
        max_length=255, blank=True, null=True)
    vads_redirect_error_timeout = models.PositiveIntegerField(
        blank=True, null=True)
    vads_redirect_error_message = models.CharField(
        max_length=255, blank=True, null=True)

    # Relations
    theme = models.ForeignKey(ThemeConfig, blank=True, null=True)
    payment_config = models.ForeignKey(
        MultiPaymentConfig, blank=True, null=True)
    custom_payment_config = models.ManyToManyField(CustomPaymentConfig)

    class Meta:
        verbose_name = "Request"
        unique_together = ("vads_trans_id", "vads_site_id", "vads_trans_date")

    def set_vads_payment_config(self):
        """
        vads_payment_config can be set only after object saving.

        A custom payment config can be set once PaymentRequest saved
        (adding elements to the m2m relationship). As a consequence
        we set vads_payment_config just before sending data elements
        to payzen."""
        self.vads_payment_config = tools.get_vads_payment_config(
            self.payment_config, self.custom_payment_config.all())

    def set_signature(self):
        self.signature = tools.get_signature(self)

    @property
    def response(self):
        try:
            return PaymentResponse.objects.get(
                vads_trans_id=self.vads_trans_id,
                vads_trans_date=self.vads_trans_date,
                vads_site_id=self.vads_site_id)
        except PaymentResponse.DoesNotExist:
            return PaymentResponse.objects.none()

    @property
    def payment_successful(self):
        return self.response and self.response.payment_successful

    def save(self):
        """
        We set up vads_trans_id and theme according to payzen format.

        If fields values are explicitely set by user, we do not override
        their values.
        """
        if not self.vads_trans_date:
            self.vads_trans_date = datetime.datetime.utcnow().replace(
                tzinfo=utc).strftime("%Y%m%d%H%M%S")
        if not self.vads_trans_id:
            self.vads_trans_id = tools.get_vads_trans_id(
                self.vads_site_id, self.vads_trans_date)
        if self.theme and not self.vads_theme_config:
            self.vads_theme_config = str(self.theme)
        if not self.pk:
            super(PaymentRequest, self).save()
        self.set_vads_payment_config()
        self.set_signature()
        super(PaymentRequest, self).save()

    def update(self):
        if not self.pk:
            # Prevent bug on filtering m2m relationship
            self.save()
        if not self.vads_trans_date:
            self.vads_trans_date = datetime.datetime.utcnow().replace(
                tzinfo=utc).strftime("%Y%m%d%H%M%S")
        self.set_vads_payment_config()
        self.set_signature()
        self.save()
