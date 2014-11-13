import json
from freezegun import freeze_time

from django.test import TestCase
from django.core.cache import cache
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from rest_framework.test import APIClient

from core import models


class TestFull(TestCase):
    def setUp(self):
        self.msisdn = '21981527318'
        self.user = User.objects.create_user('foo bar')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_user_behaviour(self):
        response = self.client.post(
            reverse('customer-list'),
            json.dumps({'msisdn': self.msisdn}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)

        response = self.client.get(reverse('customer-detail', kwargs={'msisdn': self.msisdn}))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('customer-list'))
        self.assertEqual(response.status_code, 200)

        response = self.client.delete(reverse('customer-detail', kwargs={'msisdn': self.msisdn}))
        self.assertEqual(response.status_code, 204)


class TestListCustomers(TestCase):
    def setUp(self):
        self.msisdn = '21981527318'
        self.user = User.objects.create_user('foo bar')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    @freeze_time('2014-11-10 13:00:00')
    def test_list(self):
        models.Customer.objects.create(msisdn=self.msisdn, created_by=self.user)
        cache.delete('blacklist')

        response = self.client.get(reverse('customer-list'))

        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content)

        self.assertEqual(content['count'], int(1))
        self.assertEqual(content['next'], None)
        self.assertEqual(content['previous'], None)
        self.assertTrue(content['results'][0]['id'])
        self.assertTrue(content['results'][0]['url'])
        self.assertEqual(content['results'][0]['msisdn'], int(self.msisdn))
        self.assertEqual(content['results'][0]['date_inserted'], '2014-11-10T13:00:00Z')
        self.assertEqual(content['results'][0]['created_by'], self.user.username)


class TestRetrieveCustomer(TestCase):
    def setUp(self):
        self.msisdn = '21981527318'
        self.user = User.objects.create_user('foo bar')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    @freeze_time('2014-11-10 13:00:00')
    def test_msisdn_is_blacklisted(self):
        models.Customer.objects.create(msisdn=self.msisdn, created_by=self.user)
        cache.delete('blacklist')

        response = self.client.get(reverse('customer-detail', kwargs={'msisdn': self.msisdn}))

        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content)

        self.assertTrue(content['id'])
        self.assertTrue(content['url'])
        self.assertEqual(content['msisdn'], int(self.msisdn))
        self.assertEqual(content['date_inserted'], '2014-11-10T13:00:00Z')
        self.assertEqual(content['created_by'], self.user.username)

    def test_msisdn_is_not_blacklisted(self):
        response = self.client.get(reverse('customer-detail', kwargs={'msisdn': self.msisdn}))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, '')

    def tearDown(self):
        cache.delete('blacklist')


class TestCreateCustomer(TestCase):
    def setUp(self):
        self.msisdn = '21981527318'
        self.user = User.objects.create_user('foo bar')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    @freeze_time('2014-11-10 13:00:00')
    def test_msisdn_is_valid(self):
        response = self.client.post(
            reverse('customer-list'),
            json.dumps({'msisdn': self.msisdn}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)

        content = json.loads(response.content)

        self.assertTrue(content['id'])
        self.assertTrue(content['url'])
        self.assertEqual(content['msisdn'], int(self.msisdn))
        self.assertEqual(content['date_inserted'], '2014-11-10T13:00:00Z')
        self.assertEqual(content['created_by'], self.user.username)

    def test_msisdn_length_is_not_valid(self):
        response = self.client.post(
            reverse('customer-list'),
            json.dumps({'msisdn': '21000'}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)


class TestDeleteCustomer(TestCase):
    def setUp(self):
        self.msisdn = '21981527318'
        self.user = User.objects.create_user('foo bar')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    @freeze_time('2014-11-10 13:00:00')
    def test_update_status_instead_of_deleting(self):
        customer = models.Customer.objects.create(msisdn=self.msisdn, created_by=self.user)

        response = self.client.delete(
            reverse(
                'customer-detail',
                kwargs={'msisdn': self.msisdn}
            )
        )

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, '')

        updated_customer = models.Customer.objects.get(pk=customer.pk)
        self.assertEqual(updated_customer.status, models.Customer.STATUS_DELETED)
