import logging

from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.core.cache import cache

from rest_framework.authtoken.models import Token

from core import models

logger = logging.getLogger(__name__)


@receiver(post_delete, sender=models.Customer)
@receiver(post_save, sender=models.Customer)
def delete_blacklist_from_memcached(sender, **kwargs):
    logger.info('Signal from admin: Deleting blacklist from memcached ...')
    cache.delete('blacklist')
    logger.info('Signal from admin: Blacklist deleted from memcached!')


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        logger.info('Signal from admin: Creating token for user %s ...' % (instance.username, ))
        Token.objects.create(user=instance)
        logger.info('Signal from admin: Token created!')
