# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20141113_2113'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='date_updated',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='deleted_by',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='status',
        ),
        migrations.RemoveField(
            model_name='historicalcustomer',
            name='date_updated',
        ),
        migrations.RemoveField(
            model_name='historicalcustomer',
            name='deleted_by_id',
        ),
        migrations.RemoveField(
            model_name='historicalcustomer',
            name='status',
        ),
    ]
