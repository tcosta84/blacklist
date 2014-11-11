from freezegun import freeze_time

from django.test import TestCase
from django.core.cache import cache
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from rest_framework.test import APIClient

from core import models


class TestCustomerListAPI(TestCase):
    @freeze_time('2014-11-10 13:00:00')
    def test_msisdn_is_blacklisted(self):
        user = User.objects.create_user('foo bar')
        customer = models.Customer.objects.create(msisdn='21981527318', created_by=user)

        client = APIClient()
        client.force_authenticate(user=user)

        api_url = reverse('customer-list') + '?msisdn=%s' % (customer.msisdn, )
        response = client.get(api_url)

        expected_response = '{"count": 1, "next": null, "previous": null, "results": [{"url": "http://testserver/customers/%s/", "id": %s, "msisdn": 21981527318, "date_inserted": "2014-11-10T13:00:00Z"}]}' % (customer.id, customer.id, )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, expected_response)

    def test_msisdn_is_not_blacklisted(self):
        user = User.objects.create_user('foo bar')

        client = APIClient()
        client.force_authenticate(user=user)

        api_url = reverse('customer-list') + '?msisdn=21981527318'
        response = client.get(api_url)

        expected_response = '{"count": 0, "next": null, "previous": null, "results": []}'

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, expected_response)

    def tearDown(self):
        cache.delete('blacklist')


class TestCustomerDeleteAPI(TestCase):
    @freeze_time('2014-11-10 13:00:00')
    def test_update_status_instead_of_deleting(self):
        user = User.objects.create_user('foo bar')
        customer = models.Customer.objects.create(msisdn='21981527318', created_by=user)

        client = APIClient()
        client.force_authenticate(user=user)

        response = client.delete(reverse('customer-detail', kwargs={'pk': customer.pk}))

        updated_customer = models.Customer.objects.get(pk=customer.pk)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(updated_customer.status, models.Customer.STATUS_DELETED)

    def tearDown(self):
        cache.delete('blacklist')
