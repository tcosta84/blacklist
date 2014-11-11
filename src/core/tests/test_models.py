from django.test import TestCase
from django.core.exceptions import ValidationError

from core import models


class TestCustomer(TestCase):
    def test_error_when_msisdn_has_less_than_10_digits(self):
        msisdn = 218152731
        with self.assertRaisesRegexp(ValidationError, 'MSISDN must have 10 or 11 digits'):
            models.Customer.objects.create(msisdn=msisdn)
