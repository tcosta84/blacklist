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
            ).select_related().order_by('-date_inserted')

            logger.info('Setting cache ...')
            cache.set('blacklist', data)

        self.queryset = data
        return super(MemcachedMixin, self).dispatch(request, *args, **kwargs)


class CustomerListCreateView(MemcachedMixin, APIView):
    """
    Allows client applications to list all customers currently blacklisted and also add new
    customers to the blacklist
    """

    def get(self, request, *args, **kwargs):
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

    def post(self, request, *args, **kwargs):
        logger.info('Create API')
        logger.info('User: %s' % (request.user, ))

        serializer = serializers.CustomerSerializer(data=request.DATA)
        if serializer.is_valid():
            customer = models.Customer.objects.create(
                msisdn=serializer.object.msisdn,
                created_by=request.user
            )
            serializer = serializers.CustomerSerializer(
                customer,
                context={'request': request}
            )
            cache.delete('blacklist')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerRetrieveDestroyView(MemcachedMixin, APIView):
    """
    Allows client applications to retrieve and delete a specific customer by its MSISDN
    """
    def get(self, request, *args, **kwargs):
        logger.info('Detail API')
        logger.info('User: %s' % (request.user, ))

        msisdn = kwargs['msisdn']

        logger.info('Retrieving customer info (customer id: %s) ...' % (msisdn,))

        queryset = [customer for customer in self.queryset if customer.msisdn == int(msisdn)]

        try:
            content = queryset[0]
            serializer = serializers.CustomerSerializer(content, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except IndexError:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        logger.info('Delete API')
        logger.info('User: %s' % (request.user, ))

        msisdn = kwargs['msisdn']

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
