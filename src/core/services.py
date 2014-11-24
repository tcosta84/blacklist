import logging

from django.db import connection
from django.db import transaction
from django.core.cache import cache
from django.contrib.auth.models import User

from core import models


def set_cache_is_live():
    cache.set('live', True, None)


@transaction.atomic
def retrieve_customers():
    cursor = connection.cursor()
    cursor.execute('BEGIN')

    query = 'SELECT c.id, c.msisdn, c.date_inserted, u.id, u.username FROM core_customer as c INNER JOIN auth_user as u ON (c.created_by_id = u.id) ORDER BY c.id'
    cursor.execute('DECLARE giant_cursor CURSOR FOR %s' % (query, ))
    while True:
        print 'FETCHING MORE 1000 rows ...'
        cursor.execute('FETCH 1000 FROM giant_cursor')
        rows = cursor.fetchall()

        if not rows:
            print 'No more customers to retrieve!!!'
            break

        for row in rows:
            user = User()
            user.id = row[3]
            user.username = row[4]

            customer = models.Customer()
            customer.id = row[0]
            customer.msisdn = row[1]
            customer.date_inserted = row[2]
            customer.created_by = user

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
