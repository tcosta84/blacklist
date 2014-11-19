from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from core import models


class TestCustomer(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test')

    def test_error_when_msisdn_has_less_than_12_digits(self):
        msisdn = 218152731
        with self.assertRaisesRegexp(ValidationError, 'MSISDN must have 12 or 13 digits'):
            models.Customer.objects.create(msisdn=msisdn, created_by=self.user)

    def test_error_when_msisdn_doesnot_start_with_55(self):
        msisdn = 992181527318
        with self.assertRaisesRegexp(ValidationError, 'MSISDN must start with 55'):
            models.Customer.objects.create(msisdn=msisdn, created_by=self.user)
