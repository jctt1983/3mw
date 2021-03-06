""" Helper to create test data.

source:
https://docs.djangoproject.com/en/1.11/howto/custom-management-commands/
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from datetime import date
from sites.models import Site, SiteData
import random
import decimal


class Command(BaseCommand):
    help = 'Create testing data (not for production!)'

    def handle(self, *args, **options):
        self.generate_test_data()

    def generate_test_data(self):
        sid = transaction.savepoint()
        try:
            for n in xrange(1, 21):
                s = Site(name='Site %s' % n)
                s.save()

                for m in xrange(100):
                    v1 = decimal.Decimal(random.randrange(100, 100000)) / 100
                    v2 = decimal.Decimal(random.randrange(100, 100000)) / 100
                    d = SiteData(site=s, date=date.today(), dataA=v1, dataB=v2)
                    d.save()

                msg = 'Successfully created site "%s"' % s.id
                self.stdout.write(self.style.SUCCESS(msg))
            transaction.savepoint_commit(sid)
        except Exception as e:
            transaction.savepoint_rollback(sid)
            msg = 'Failed to complete this process: ' + str(e)
            self.stdout.write(self.style.ERROR(msg))
