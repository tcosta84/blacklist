import logging

from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from core import models, serializers

logger = logging.getLogger(__name__)


class MemcachedMixin(object):
    def dispatch(self, request, *args, **kwargs):
        data = cache.get('blacklist')
        if data is None:
            logger.info('Blacklist is not cached. Retrieving updated blacklist to set cache ...')
            data = models.Customer.objects.filter(
                status=models.Customer.STATUS_ACTIVE
            ).order_by('-date_inserted')

            logger.info('Setting cache ...')
            cache.set('blacklist', data)

        self.queryset = data
        return super(MemcachedMixin, self).dispatch(request, *args, **kwargs)


class RootAPI(MemcachedMixin, APIView):
    pass


class CustomerListView(MemcachedMixin, APIView):
    """
    Allows client applications to retrieve all customers currently blacklisted
    """
    def get(self, request):
        logger.info('List API')
        logger.info('User: %s' % (request.user, ))

        page = request.QUERY_PARAMS.get('page')
        page_size = request.QUERY_PARAMS.get('page_size')

        if not page_size:
            page_size = settings.REST_FRAMEWORK['PAGINATE_BY']

        paginator = Paginator(self.queryset, page_size)
        try:
            page_content = paginator.page(page)
        except PageNotAnInteger:
            page_content = paginator.page(1)
        except EmptyPage:
            page_content = paginator.page(paginator.num_pages)

        serializer = serializers.PaginatedCustomerSerializer(
            page_content, 
            context={'request': request}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomerDetailView(MemcachedMixin, APIView):
    """
    Allows client applications to retrieve and delete a customer by its MSISDN
    """
    def get(self, request, msisdn):
        logger.info('Detail API')
        logger.info('User: %s' % (request.user, ))
        logger.info('Retrieving customer info (customer id: %s) ...' % (msisdn,))

        queryset = [customer for customer in self.queryset if customer.msisdn == int(msisdn)]

        try:
            content = queryset[0]
            serializer = serializers.CustomerSerializer(content, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except IndexError:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, msisdn):
        logger.info('Delete API')
        logger.info('User: %s' % (request.user, ))
        logger.info('Updating customer status (customer id: %s) ...' % (msisdn,))

        models.Customer.objects.filter(
            msisdn=msisdn,
            status=models.Customer.STATUS_ACTIVE
        ).update(
            status=models.Customer.STATUS_DELETED,
            deleted_by=request.user
        )

        logger.info('Deleting blacklist from memcached ...')
        cache.delete('blacklist')
        return Response(status=status.HTTP_204_NO_CONTENT)
