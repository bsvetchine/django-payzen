"""
Models for Payzen - Payment using webform v2

The models are implemented according to the document :
'Guide_d_implementation_formulaire_paiement_V2_Payzen_v2.9f.pdf'

TODO add validators to manage payzen contraints on special fields.
"""

import datetime

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from . import app_settings
from . import tools


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


class PaymentRequest(CustomerDetails, OrderDetails, ShippingDetails):
    """Model that contains all Payzen parameters to initiate a payment.

    The first 7 fields are mandatory, all others are optional.
    """

    VADS_ACTION_MODE_CHOICES = (
        ('INTERACTIVE', 'INTERACTIVE'),
        ('SILENT', 'SILENT'),
    )

    VADS_CURRENCY_CHOICES = (
        ('036', 'Australian dollar'),
        ('124', 'Canadian dollar'),
        ('156', 'Chinese Yuan'),
        ('208', 'Danish Krone'),
        ('392', 'Japanese Yen'),
        ('578', 'Norwegian Krone'),
        ('752', 'Swedish Krona'),
        ('756', 'Swiss franc'),
        ('826', 'Pound sterling'),
        ('840', 'American dollar'),
        ('953', 'Franc Pacifique (CFP)'),
        ('978', 'Euro')
    )

    VADS_CTX_MODE_CHOICES = (
        ('TEST', 'TEST'),
        ('PRODUCTION', 'PRODUCTION')
    )

    VADS_RETURN_MODE_CHOICES = (
        ('AMEX', 'American Express'),
        ('AURORE-MULTI', 'AURORE (multi brand)'),
        ('BUYSTER', 'BUYSTER'),
        ('CB', 'CB'),
        ('COFINOGA', 'COFINOGA'),
        ('E-CARTEBLEUE', 'e blue card'),
        ('MASTERCARD', 'Eurocard / MasterCard'),
        ('JCB', 'JCB'),
        ('MAESTRO', 'Maestro'),
        ('ONEY', 'ONEY'),
        ('ONEY_SANDBOX', 'ONEY SANDBOX mode'),
        ('PAYPAL', 'PAYPAL'),
        ('PAYPAL_SB', 'PAYPAL SANDBOX mode'),
        ('PAYSAFECARD', 'PAYSAFECARD'),
        ('VISA', 'Visa'),
        ('VISA_ELECTRON', 'Visa Electron'),
        ('COF3XCB', '3x CB Cofinoga'),
        ('COF3XCB_SB', '3x CB Cofinoga SANDBOX'),
    )

    VADS_VALIDATION_MODE_CHOICES = (
        ('', 'Default shop configuration (using payzen admin)'),
        ('0', 'Automatic validation'),
        ('1', 'Manual validation')
    )

    # Mandatory fields
    vads_action_mode = models.CharField(
        max_length=11, choices=VADS_ACTION_MODE_CHOICES,
        default=app_settings.VADS_ACTION_MODE)
    vads_amount = models.PositiveIntegerField()
    vads_currency = models.CharField(
        max_length=3, choices=VADS_CURRENCY_CHOICES,
        default=app_settings.VADS_CURRENCY)
    vads_ctx_mode = models.CharField(
        max_length=10, choices=VADS_CTX_MODE_CHOICES,
        default=app_settings.VADS_CTX_MODE)
    vads_page_action = models.CharField(
        max_length=7, default='PAYMENT')
    vads_payment_config = models.TextField()
    vads_site_id = models.PositiveIntegerField(
        default=app_settings.VADS_SITE_ID)
    vads_trans_date = models.CharField(
        max_length=14,
        default=datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S"))
    vads_trans_id = models.CharField(max_length=6)
    vads_version = models.CharField(
        max_length=2, default='V2')
    signature = models.CharField(
        max_length=40)
    # Optional fields
    vads_capture_delay = models.PositiveIntegerField(blank=True, null=True)
    vads_contrib = models.CharField(
        max_length=255, blank=True, null=True,
        default=app_settings.VADS_CONTRIB)
    vads_payment_cards = models.CharField(
        max_length=127, blank=True, null=True)
    vads_return_mode = models.CharField(
        max_length=12, choices=VADS_RETURN_MODE_CHOICES, blank=True, null=True)
    vads_theme_config = models.CharField(
        max_length=255, blank=True, null=True)
    vads_validation_mode = models.CharField(
        choices=VADS_VALIDATION_MODE_CHOICES,
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

    def save(self):
        """
        We set up vads_trans_id and theme according to payzen format.

        If fields values are explicitely set by user, we do not override
        their values.
        """
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
        self.set_vads_payment_config()
        self.set_signature()
        self.save()
