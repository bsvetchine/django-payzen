from django import forms

from . import models


class PaymentRequestForm(forms.ModelForm):

    class Meta:
        model = models.PaymentRequest
        exclude = []

    def __remove_empty_fields(self):
        form_fields_to_remove = []
        for model_field_name, form_field in self.fields.items():
            if not getattr(self.instance, model_field_name):
                form_fields_to_remove.append(model_field_name)
        for model_field_name in form_fields_to_remove:
            self.fields.pop(model_field_name)

    def __set_all_fields_hidden(self):
        for field in self.fields.values():
            field.widget = forms.HiddenInput()

    def __init__(self, *args, **kwargs):
        super(PaymentRequestForm, self).__init__(*args, **kwargs)
        self.__remove_empty_fields()
        self.__set_all_fields_hidden()


class PaymentResponseForm(forms.ModelForm):

    class Meta:
        model = models.PaymentResponse
        exclude = []
