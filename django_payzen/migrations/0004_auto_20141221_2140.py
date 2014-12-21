# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_payzen', '0003_auto_20141027_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentrequest',
            name='vads_contrib',
            field=models.CharField(default=b'django-payzen v1.0', max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
