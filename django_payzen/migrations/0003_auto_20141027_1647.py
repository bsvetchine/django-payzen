# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_payzen', '0002_auto_20141024_0822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentresponse',
            name='vads_url_check_src',
            field=models.CharField(blank=True, max_length=10, null=True, choices=[(b'PAY', b'PAY'), (b'BO', b'BO'), (b'BATCH', b'BATCH'), (b'BATCH_AUTO', b'BATCH_AUTO'), (b'FILE', b'FILE'), (b'REC', b'REC'), (b'MERCH_BO', b'MERCH_BO')]),
            preserve_default=True,
        ),
    ]
