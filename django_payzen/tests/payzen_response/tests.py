import time

from django import template
from django.test import LiveServerTestCase

from .. import data
from ... import models

from selenium.webdriver.firefox import webdriver
from selenium.common import exceptions


class PayzenResponseTester(object):

    @classmethod
    def setUpClass(cls):
        cls.selenium = webdriver.WebDriver()
        super(PayzenResponseTester, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(PayzenResponseTester, cls).tearDownClass()

    def generate_payment_form(self):
        t = template.Template(
            "{% load payzen_extras %}{% payzen_form instance %}")
        c = template.Context({
            "instance": self.instance
        })
        test = open("/tmp/payment_form_testing.html", "w")
        test.write(t.render(c))
        test.close()

    def validate_payment_form(self):
        self.selenium.get("file:///tmp/payment_form_testing.html")
        self.selenium.find_element_by_xpath('//input[@type="submit"]').click()

    def select_payment_card(self):
        self.selenium.find_element_by_id(
            'validationButtonPaymentMean').click()

    def enter_card_number(self):
        self.selenium.find_element_by_xpath(
            '//input[@name="vads_card_number"]').send_keys(
            self.card['card_number'])
        self.selenium.find_element_by_xpath(
            '//select[@name="vads_expiry_month"]/option[@value="12"]').click()
        self.selenium.find_element_by_xpath(
            '//select[@name="vads_expiry_year"]/option[@value="2024"]').click()
        self.selenium.find_element_by_xpath(
            '//input[@name="vads_cvv"]').send_keys("123")
        self.selenium.find_element_by_id("validationButtonCard").click()

    def response_object_tester(self):
        resp = models.PaymentResponse.objects.get(
            vads_trans_id=self.instance.vads_trans_id)
        for field_name, value in self.data.items():
            if hasattr(resp, field_name):
                self.assertEqual(str(getattr(resp, field_name)), value)
        if self.card['result'] == 'accepted':
            self.assertTrue(resp.payment_successful)
        else:
            self.assertFalse(resp.payment_successful)

    def test_payzen_response(self):
        self.assertFalse(
            self.instance.payment_successful)
        self.generate_payment_form()
        self.validate_payment_form()
        try:
            self.select_payment_card()
        except exceptions.NoSuchElementException:
            # For a recurring payment, there is no card selection step
            pass
        self.enter_card_number()
        time.sleep(10)  # Wait for confirmation request from Payzen
        self.response_object_tester()
        self.assertTrue(
            self.instance.payment_successful)


class BasicPaymentTest(PayzenResponseTester, LiveServerTestCase):

    def setUp(self):
        self.data = data.payment_args
        self.instance = models.PaymentRequest(
            **data.payment_args)
        self.instance.save()
        self.card = data.cards[0]


class CustomizedPaymentTest(PayzenResponseTester, LiveServerTestCase):

    def setUp(self):
        self.data = data.payment_args
        self.instance = models.PaymentRequest(
            **data.payment_args)
        self.instance.theme = models.ThemeConfig(
            **data.theme_args)
        self.instance.theme.save()
        self.instance.payment_config = models.MultiPaymentConfig(
            **data.payment_config_args)
        self.instance.payment_config.save()
        self.instance.save()
        self.css_class_to_find = "echeancier"
        self.card = data.cards[0]
