import mock

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from core import models


class TestCustomer(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test')

    def test_unicode(self):
        customer = models.Customer()
        customer.msisdn = 5521981527318
        self.assertEqual('5521981527318', unicode(customer))

    @mock.patch('django.db.models.Model.save')
    @mock.patch('django.db.models.Model.full_clean')
    def test_save(self, full_clean_mock, save_mock):
        customer = models.Customer()

        args = []
        kwargs = {}
        customer.save(*args, **kwargs)

        full_clean_mock.assert_called_with()
        save_mock.assert_called_with(*args, **kwargs)

    def test_error_when_msisdn_has_less_than_12_digits(self):
        msisdn = 218152731
        with self.assertRaisesRegexp(ValidationError, 'MSISDN must have 12 or 13 digits'):
            models.Customer.objects.create(msisdn=msisdn, created_by=self.user)

    def test_error_when_msisdn_doesnot_start_with_55(self):
        msisdn = 9921981527318
        with self.assertRaisesRegexp(ValidationError, 'MSISDN must start with 55'):
            models.Customer.objects.create(msisdn=msisdn, created_by=self.user)

    def test_error_when_msisdn_has_more_than_13_digits(self):
        msisdn = 55219815273188
        with self.assertRaisesRegexp(ValidationError, 'MSISDN must have 12 or 13 digits. Given: 14'):
            models.Customer.objects.create(msisdn=msisdn, created_by=self.user)


class TestCustomerHistory(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test')

    def test_unicode(self):
        customer_history = models.CustomerHistory()
        customer_history.msisdn = 5521981527318
        customer_history.action = models.CustomerHistory.ACTION_CREATE

        self.assertEqual('5521981527318, Create', unicode(customer_history))
