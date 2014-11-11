from django.db import models
from django.contrib.auth.models import User

from core import validators


class Customer(models.Model):
    STATUS_ACTIVE = 1
    STATUS_DELETED = -1
    STATUS_CHOICES = (
        (STATUS_ACTIVE, 'Active'),
        (STATUS_DELETED, 'Deleted'),
    )

    msisdn = models.BigIntegerField(validators=[validators.validate_msisdn])
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    created_by = models.ForeignKey(User, related_name='created_by', editable=False)
    deleted_by = models.ForeignKey(User, null=True, related_name='deleted_by', editable=False)
    date_inserted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Customer, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s' % (self.msisdn, )
