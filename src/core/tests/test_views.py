import mock
from freezegun import freeze_time

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from rest_framework.test import APIRequestFactory, force_authenticate

from core import views, models


class CustomerRetrieveDestroyView(TestCase):
    def setUp(self):
        self.msisdn = '5521981527318'
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='tester')
        self.view = views.CustomerRetrieveDestroyView.as_view()
    
    @mock.patch('core.views.cache.get', autospec=True)
    def test_get_cache_exists(self, cache_get):

        # given
        request = self.factory.get('customer-detail')
        force_authenticate(request, user=self.user)
        
        customer_mock = mock.Mock()
        customer_mock.msisdn = self.msisdn
        customer_mock.date_inserted = mock.Mock()
        customer_mock.created_by = self.user
        
        cache_get.return_value = customer_mock
        
        # when
        args = []
        kwargs = {'msisdn': self.msisdn}
        response = self.view(request, *args, **kwargs)
       
        # then
        cache_get.assert_called_with(self.msisdn)
    
    @mock.patch('core.views.cache.get', autospec=True)
    def test_get_cache_does_not_exist(self, cache_get):

        # given
        request = self.factory.get('customer-detail')
        force_authenticate(request, user=self.user)
        
        customer_mock = mock.Mock()
        customer_mock.msisdn = self.msisdn
        customer_mock.date_inserted = mock.Mock()
        customer_mock.created_by = self.user
        
        cache_get.return_value = None
        
        # when
        args = []
        kwargs = {'msisdn': self.msisdn}
        response = self.view(request, *args, **kwargs)
       
        # then
        cache_get.assert_called_with('live')

    @mock.patch('core.models.CustomerHistory.objects.create', autospec=True)
    @mock.patch('core.models.Customer.objects.get', autospec=True)
    @mock.patch('core.views.cache.delete', autospec=True)
    def test_delete(self, cache_delete, customer_model_get, 
            customer_history_model_create):

        # given
        request = self.factory.delete('customer-detail')
        force_authenticate(request, user=self.user)
        
        customer_mock = mock.Mock()
        customer_mock.msisdn = self.msisdn
        customer_mock.date_inserted = mock.Mock()
        customer_mock.created_by = self.user
        customer_model_get.return_value = customer_mock
        
        # when
        args = []
        kwargs = {'msisdn': self.msisdn}
        response = self.view(request, *args, **kwargs)
       
        # then
        customer_model_get.assert_called_with(msisdn=self.msisdn)
        
        customer_mock.delete.assert_called_with()
        
        customer_history_model_create.assert_called_with(
            msisdn=customer_mock.msisdn,
            created_by=customer_mock.created_by, 
            date_inserted=customer_mock.date_inserted,
            action=models.CustomerHistory.ACTION_DELETE, 
            history_changed_by=self.user
        )
        
        cache_delete.assert_called_with(customer_mock.msisdn)
