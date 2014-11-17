from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from core import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.first()

        for i in xrange(1000000):
            msisdn = '21' + str(i).rjust(9, '0')
            print int(msisdn)
            models.Customer.objects.create(msisdn=int(msisdn), created_by=user)
