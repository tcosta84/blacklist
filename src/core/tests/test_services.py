import mock

from django.test import TestCase

from core import services


class TestPopulateMemcached(TestCase):
    @mock.patch('core.services.cache.get', autospec=True)
    @mock.patch('core.services.set_cache_is_live', cutospec=True)
    @mock.patch('core.services.retrieve_customers', autospec=True)
    def test_should_retrieve_customers_when_cache_is_not_live(self, retrieve_customers,
            set_cache_is_live, cache):

        cache.return_value = None
        services.populate_memcached()
        self.assertTrue(retrieve_customers.called)
        self.assertTrue(set_cache_is_live.called)

    @mock.patch('core.services.cache.get', autospec=True)
    @mock.patch('core.services.set_cache_is_live', cutospec=True)
    @mock.patch('core.services.retrieve_customers', autospec=True)
    def test_should_do_nothing_when_cache_is_live(self, retrieve_customers,
            set_cache_is_live, cache):

        cache.return_value = True
        services.populate_memcached()
        self.assertFalse(retrieve_customers.called)
        self.assertFalse(set_cache_is_live.called)


class TestSetCacheIsLive(TestCase):
    @mock.patch('core.services.cache.set', autospec=True)
    def test_should_set_cache(self, cache):
        services.set_cache_is_live()
        cache.assert_called_with('live', True, None)
