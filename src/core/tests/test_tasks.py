import mock

from django.test import TestCase

from core import tasks


class TestPopulateMemcached(TestCase):
    @mock.patch('core.services.populate_memcached', autospec=True)
    def test_should_execute_task(self, service):
        tasks.populate_memcached()

        service.assert_called_with()

    @mock.patch('core.tasks.populate_memcached.retry', autospec=True)
    @mock.patch('core.services.populate_memcached', autospec=True)
    def test_should_retry_task(self, service, task_retry):
        e = Exception('Boom')
        service.side_effect = e

        try:
            tasks.populate_memcached()
        except:
            pass

        task_retry.assert_called_with(exc=e, countdown=10)
