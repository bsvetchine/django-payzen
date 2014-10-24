# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_payzen', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentresponse',
            name='vads_action_mode',
            field=models.CharField(blank=True, max_length=11, null=True, choices=[(b'INTERACTIVE', b'INTERACTIVE'), (b'SILENT', b'SILENT')]),
        ),
        migrations.AlterField(
            model_name='paymentresponse',
            name='vads_contract_used',
            field=models.CharField(max_length=250, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='paymentresponse',
            name='vads_result',
            field=models.CharField(max_length=2, choices=[(b'00', b'Payment successful'), (b'02', b'Merchant should contact his bank'), (b'05', b'Payment refused'), (b'17', b'Payment cancelled by client'), (b'30', b'Wrong request format'), (b'96', b'Technical error during payment process')]),
        ),
        migrations.AlterField(
            model_name='paymentresponse',
            name='vads_url_check_src',
            field=models.CharField(max_length=10, choices=[(b'PAY', b'PAY'), (b'BO', b'BO'), (b'BATCH', b'BATCH'), (b'BATCH_AUTO', b'BATCH_AUTO'), (b'FILE', b'FILE'), (b'REC', b'REC'), (b'MERCH_BO', b'MERCH_BO')]),
        ),
    ]
