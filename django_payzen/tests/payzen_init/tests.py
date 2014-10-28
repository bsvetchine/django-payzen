from django import template
from django.test import LiveServerTestCase

from .. import data
from ... import models

from selenium.webdriver.firefox import webdriver


class PaymentInitTester(object):

    @classmethod
    def setUpClass(cls):
        cls.selenium = webdriver.WebDriver()
        super(PaymentInitTester, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(PaymentInitTester, cls).tearDownClass()

    def generate_payment_form(self):
        t = template.Template(
            "{% load payzen_extras %}{% payzen_form instance %}")
        c = template.Context({
            "instance": self.instance
        })
        test = open("/tmp/payment_form_testing.html", "w")
        test.write(t.render(c))
        test.close()

    def payment_form_test(self):
        self.selenium.get("file:///tmp/payment_form_testing.html")
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()

    def payzen_form_test(self):
        self.assertTrue(
            self.selenium.current_url.startswith("https://secure.payzen.eu"))
        for css_class in self.css_classes_to_find:
            self.selenium.find_element_by_class_name(css_class)

    def test_payment_initialization(self):
        self.generate_payment_form()
        self.payment_form_test()
        self.payzen_form_test()


class BasicPaymentTest(PaymentInitTester, LiveServerTestCase):

    def setUp(self):
        self.instance = models.PaymentRequest(
            **data.payment_args)
        self.instance.save()
        self.css_classes_to_find = [
            "cardNumber", "vads-expiry-date-input", "validationButton", ]


class CustomizedPaymentTest(PaymentInitTester, LiveServerTestCase):

    def setUp(self):
        self.instance = models.PaymentRequest(
            **data.payment_args)
        self.instance.theme = models.ThemeConfig(
            **data.theme_args)
        self.instance.theme.save()
        self.instance.payment_config = models.MultiPaymentConfig(
            **data.payment_config_args)
        self.instance.payment_config.save()
        self.instance.save()
        self.css_classes_to_find = [
            "echeancier", "cardNumber", "vads-expiry-date-input",
            "validationButton", ]
