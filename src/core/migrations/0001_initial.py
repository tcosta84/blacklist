# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('msisdn', models.BigIntegerField(validators=[core.validators.validate_msisdn])),
                ('status', models.SmallIntegerField(default=1, choices=[(1, b'Active'), (-1, b'Deleted')])),
                ('date_inserted', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(related_name='created_by', to=settings.AUTH_USER_MODEL)),
                ('deleted_by', models.ForeignKey(related_name='deleted_by', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
