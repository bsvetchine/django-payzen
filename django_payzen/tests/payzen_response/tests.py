import time

from django import template
from django.test import LiveServerTestCase

from .. import data
from ... import models

from selenium.webdriver.firefox import webdriver


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
        resp = models.PaymentRequest.objects.get(
            vads_trans_id=self.data['vads_trans_id'])
        for field_name, value in self.data.items():
            self.assertEqual(getattr(resp, field_name), value)

    def test_payzen_response(self):
        self.generate_payment_form()
        self.validate_payment_form()
        self.select_payment_card()
        self.enter_card_number()
        time.sleep(5)
        self.response_object_tester()


class BasicPaymentTest(PayzenResponseTester, LiveServerTestCase):

    def setUp(self):
        self.data = data.basic_payment_args
        self.instance = models.PaymentRequest(**self.data)
        self.instance.save()
        self.card = data.cards[0]
