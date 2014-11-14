# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20141114_0035'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customerhistory',
            options={'verbose_name_plural': 'Customer Histories'},
        ),
        migrations.AddField(
            model_name='customerhistory',
            name='history_date_inserted',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 14, 0, 58, 55, 389011, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customerhistory',
            name='created_by',
            field=models.ForeignKey(related_name='history_created_by', editable=False, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
