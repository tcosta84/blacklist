import mock

from django.test import TestCase
from django.core.management import call_command


class TestPopulateMemcached(TestCase):
    @mock.patch('core.services.populate_memcached', autospec=True)
    def test_should_populate_memcached(self, populate_memcached):
        args = []
        opts = {}
        call_command('populate_memcached', *args, **opts)
        self.assertTrue(populate_memcached.called)
