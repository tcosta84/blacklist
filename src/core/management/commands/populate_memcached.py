from django.core.management.base import BaseCommand

from core import services


class Command(BaseCommand):
    def handle(self, *args, **options):
        services.populate_memcached()
