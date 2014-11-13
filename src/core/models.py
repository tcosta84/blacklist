from django.db import models
from django.contrib.auth.models import User

from simple_history.models import HistoricalRecords

from core import validators


class Customer(models.Model):
    msisdn = models.BigIntegerField(unique=True, validators=[validators.validate_msisdn])
    created_by = models.ForeignKey(User, related_name='created_by', editable=False)
    date_inserted = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Customer, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s' % (self.msisdn, )
