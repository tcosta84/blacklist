from django.core.management.base import BaseCommand
from django.core.cache import cache


class Command(BaseCommand):
    def handle(self, *args, **options):
        if cache.get('blacklist'):
            print 'Deleting "blacklist" key from cache ...'
            deleted = cache.delete('blacklist')
            if deleted:
                print 'Key "blacklist" deleted!'
        else:
            print 'Key "blacklist" is already empty. Theres nothing to delete!'
