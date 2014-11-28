from django.db import models
from django.contrib.auth.models import User

from core import validators


class Customer(models.Model):
    msisdn = models.BigIntegerField(unique=True, validators=[validators.validate_msisdn],
            help_text='55 + DDD + Number')
    created_by = models.ForeignKey(User, related_name='created_by', editable=False)
    date_inserted = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Customer, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s' % (self.msisdn, )


class CustomerHistory(models.Model):
    ACTION_CREATE = 1
    ACTION_DELETE = -1
    ACTION_CHOICES = (
        (ACTION_CREATE, 'Create'),
        (ACTION_DELETE, 'Delete')
    )

    msisdn = models.BigIntegerField()
    created_by = models.ForeignKey(User, related_name='history_created_by', editable=False)
    date_inserted = models.DateTimeField()
    action = models.SmallIntegerField(choices=ACTION_CHOICES)
    history_changed_by = models.ForeignKey(User)
    history_date_inserted = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s, %s' % (self.msisdn, self.get_action_display())

    class Meta:
        verbose_name_plural = 'Customer Histories'
