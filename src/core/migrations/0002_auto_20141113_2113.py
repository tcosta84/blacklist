# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalCustomer',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('msisdn', models.BigIntegerField(db_index=True, validators=[core.validators.validate_msisdn])),
                ('status', models.SmallIntegerField(default=1, choices=[(1, b'Active'), (-1, b'Deleted')])),
                ('created_by_id', models.IntegerField(db_index=True, null=True, editable=False, blank=True)),
                ('deleted_by_id', models.IntegerField(db_index=True, null=True, editable=False, blank=True)),
                ('date_inserted', models.DateTimeField(editable=False, blank=True)),
                ('date_updated', models.DateTimeField(editable=False, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'verbose_name': 'historical customer',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='customer',
            name='created_by',
            field=models.ForeignKey(related_name='created_by', editable=False, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customer',
            name='deleted_by',
            field=models.ForeignKey(related_name='deleted_by', editable=False, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='customer',
            name='msisdn',
            field=models.BigIntegerField(unique=True, validators=[core.validators.validate_msisdn]),
            preserve_default=True,
        ),
    ]
