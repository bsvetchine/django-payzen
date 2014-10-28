import datetime

from django.test import TestCase
from django import template

from .. import data
from ... import models


class RequestDataTester(object):

    def analyze_template_tag_response(self, response):
        # Test that nothing is added before template tag
        self.assertTrue(
            response.find('<form action=' +
                          '"https://secure.payzen.eu/vads-payment/"' +
                          ' method="post">') == 0)
        # Test that nothing is added after template tag
        self.assertEqual(
            response[-8:], u'</form>\n')
        # test that all fields are present
        self.assertEqual(
            response.count("input"),
            self.expected_values['fields_nb'])

    def test_payzen_form_template_tag(self):
        t = template.Template(
            "{% load payzen_extras %}{% payzen_form instance %}")
        c = template.Context({
            "instance": self.instance
        })
        response = t.render(c)
        self.analyze_template_tag_response(response)

    def test_vads_theme_config_value(self):
        self.assertEqual(
            self.expected_values['vads_theme_config'],
            self.instance.vads_theme_config)

    def test_vads_payment_config_value(self):
        self.assertEqual(
            self.expected_values['vads_payment_config'],
            self.instance.vads_payment_config)

    def test_signature_value(self):
        self.assertTrue(
            self.instance.signature and len(self.instance.signature) == 40
        )


class BasicPaymentTest(RequestDataTester, TestCase):

    def setUp(self):
        self.instance = models.PaymentRequest(
            **data.payment_args)
        self.instance.save()
        self.expected_values = {
            "fields_nb": 56,
            "vads_theme_config": None,
            "vads_payment_config": "SINGLE",
            "vads_trans_id": "000001"
        }


class CustomizedPaymentTest(RequestDataTester, TestCase):

    def setUp(self):
        self.instance = models.PaymentRequest(
            **data.payment_args)
        self.instance.payment_config = models.MultiPaymentConfig(
            **data.payment_config_args)
        self.instance.payment_config.save()
        self.instance.save()

        self.expected_values = {
            "fields_nb": 57,
            "vads_theme_config": None,
            "vads_payment_config": "MULTI:first=5000;count=2;period=5",
            "vads_trans_id": "000001"
        }


class CustomizedThemeTest(RequestDataTester, TestCase):

    def setUp(self):
        self.instance = models.PaymentRequest(
            **data.payment_args)
        self.instance.theme = models.ThemeConfig(
            **data.theme_args)
        self.instance.theme.save()
        self.instance.save()

        self.expected_values = {
            "fields_nb": 58,
            "vads_theme_config": self.get_theme_string(),
            "vads_payment_config": "SINGLE",
            "vads_trans_id": "000001"
        }

    def get_theme_string(self):
        theme_string = ""
        for key, value in data.theme_args.items():
            theme_string += "{}={};".format(
                key.upper(), value)
        return theme_string[:-1]


class MultiPaymentConfigTest(RequestDataTester, TestCase):

    def setUp(self):
        self.instance = models.PaymentRequest(
            **data.payment_args)
        self.instance.save()
        for i in range(1, 6):
            cpc = models.CustomPaymentConfig(
                date=datetime.date(2015, i, 1),
                amount=200)
            cpc.save()
            self.instance.custom_payment_config.add(cpc)
        self.instance.update()

        self.expected_values = {
            "fields_nb": 56,
            "vads_theme_config": None,
            "vads_payment_config": "MULTI_EXT:20150101=200;" +
                                   "20150201=200;" +
                                   "20150301=200;" +
                                   "20150401=200;" +
                                   "20150501=200",
            "vads_trans_id": "000001"
        }
