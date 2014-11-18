import logging

from django.db import connection
from django.db import transaction
from django.core.cache import cache

from core import models


def set_cache_is_live():
    cache.set('live', True, None)


@transaction.atomic
def retrieve_customers():
    cursor = connection.cursor()
    cursor.execute('BEGIN')

    query = 'SELECT id, msisdn, date_inserted, created_by_id FROM core_customer ORDER BY id'
    cursor.execute('DECLARE giant_cursor CURSOR FOR %s' % (query, ))
    while True:
        print 'FETCHING MORE 1000 rows ...'
        cursor.execute('FETCH 1000 FROM giant_cursor')
        rows = cursor.fetchall()

        if not rows:
            print 'No more customers to retrieve!!!'
            break

        for row in rows:
            customer = models.Customer()
            customer.id = row[0]
            customer.msisdn = row[1]
            customer.date_inserted = row[2]
            customer.created_by_id = row[3]
            print 'Setting cache for msisdn %s' % (customer.msisdn, )
            cache.set(str(row[1]), customer)

    cursor.execute('COMMIT')


def populate_memcached():
    cache_is_live = cache.get('live')
    if cache_is_live:
        logging.info('Cache is live')
    else:
        logging.info('Cache is not live')
        retrieve_customers()
        set_cache_is_live()
