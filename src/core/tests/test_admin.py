import mock

from django.test import TestCase
from django.contrib.admin.sites import AdminSite

from core import models, admin


class CustomerAdminTest(TestCase):
    @mock.patch('core.services.cache.set', autospec=True)
    @mock.patch('core.services.cache.delete', autospec=True)
    def test_save_model_change_true(self, cache_delete, cache_set):
        # given
        customer_admin = admin.CustomerAdmin(models.Customer, AdminSite())

        request = mock.Mock()
        request.user = mock.Mock()

        obj = mock.Mock()
        obj.msisdn = 21981527318

        form = mock.Mock()
        change = True

        # when
        customer_admin.save_model(request, obj, form, change)

        # then
        cache_delete.assert_called_with(str(obj.msisdn))
        obj.save.assert_called_with()
        cache_set.assert_called_with(str(obj.msisdn), obj, None)

    @mock.patch('core.services.cache.set', autospec=True)
    @mock.patch('core.services.cache.delete', autospec=True)
    def test_save_model_change_false(self, cache_delete, cache_set):
        # given
        customer_admin = admin.CustomerAdmin(models.Customer, AdminSite())

        request = mock.Mock()
        request.user = 'qwerty'

        obj = mock.Mock()
        obj.msisdn = 21981527318

        form = mock.Mock()
        change = False

        # when
        customer_admin.save_model(request, obj, form, change)

        # then
        self.assertEqual(obj.created_by, request.user)
        cache_delete.assert_called_with(str(obj.msisdn))
        obj.save.assert_called_with()
        cache_set.assert_called_with(str(obj.msisdn), obj, None)

    @mock.patch('core.services.cache.delete', autospec=True)
    @mock.patch('core.models.CustomerHistory.objects.create', autospec=True)
    def test_delete_selected(self, model_create, cache_delete):
        # given
        customer_admin = admin.CustomerAdmin(models.Customer, AdminSite())

        request = mock.Mock()
        request.user = mock.Mock()

        obj = mock.Mock()
        obj.msisdn = 5521981527318
        obj.date_inserted = ''
        obj.created_by = mock.Mock()

        queryset = mock.Mock()
        queryset.__iter__ = mock.Mock(return_value = iter([obj, ]))

        # when
        customer_admin.delete_selected(request, queryset)

        # then
        obj.delete.assert_called_with()
        cache_delete.assert_called_with(obj.msisdn)
        model_create.assert_called_with(
            msisdn=obj.msisdn,
            created_by=obj.created_by, 
            date_inserted=obj.date_inserted,
            action=models.CustomerHistory.ACTION_DELETE, 
            history_changed_by=request.user
        )
