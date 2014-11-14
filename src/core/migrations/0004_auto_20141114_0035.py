# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0003_auto_20141113_2132'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('msisdn', models.BigIntegerField()),
                ('created_by', models.IntegerField()),
                ('date_inserted', models.DateTimeField()),
                ('action', models.SmallIntegerField(choices=[(1, b'Create'), (-1, b'Delete')])),
                ('history_changed_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='historicalcustomer',
            name='history_user',
        ),
        migrations.DeleteModel(
            name='HistoricalCustomer',
        ),
    ]
