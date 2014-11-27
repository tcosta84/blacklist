from celery import shared_task
from celery.utils.log import get_task_logger

from core import services


logger = get_task_logger(__name__)


@shared_task(bind=True)
def populate_memcached(self):
    logger.info('Start task')
    try:
        services.populate_memcached()
    except Exception as e:
        logger.error('Error [%s]. Retrying ...' % (e, ))
        raise self.retry(exc=e, countdown=10)
    logger.info('End task')
