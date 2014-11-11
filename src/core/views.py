import logging

from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from core import models, serializers

logger = logging.getLogger(__name__)


class CustomerAPISet(viewsets.ViewSet):
    """
    API endpoint that allows blacklisted customers to be viewed or edited.
    """

    def dispatch(self, request, *args, **kwargs):
        """
        This method checks if blacklist is on memcached. If not, set it.
        This method is always invoked before each API request.
        """
        blacklist = cache.get('blacklist')
        if blacklist is None:
            logger.info('Blacklist is not cached. Retrieving updated blacklist to set cache ...')

            blacklist = models.Customer.objects.filter(
                    status=models.Customer.STATUS_ACTIVE).order_by('-date_inserted')

            logger.info('Setting cache ...')
            cache.set('blacklist', blacklist, None)

        self.blacklist = blacklist
        return super(CustomerAPISet, self).dispatch(request, *args, **kwargs)

    def list(self, request):
        logger.info('List API')
        logger.info('User: %s' % (request.user, ))

        queryset = self.blacklist

        page = request.QUERY_PARAMS.get('page')
        page_size = request.QUERY_PARAMS.get('page_size')
        msisdn = request.QUERY_PARAMS.get('msisdn', None)

        if msisdn is not None:
            logger.info('Filtering results by msisdn %s ...' % (msisdn, ))
            queryset = [customer for customer in self.blacklist if customer.msisdn == int(msisdn)]

        if not page_size:
            page_size = settings.REST_FRAMEWORK['PAGINATE_BY']

        paginator = Paginator(queryset, page_size)
        try:
            customers = paginator.page(page)
        except PageNotAnInteger:
            customers = paginator.page(1)
        except EmptyPage:
            customers = paginator.page(paginator.num_pages)

        serializer = serializers.PaginatedCustomerSerializer(customers, 
                context={'request':request})
        return Response(serializer.data, status=200)

    def retrieve(self, request, pk=None):
        logger.info('Detail API')
        logger.info('User: %s' % (request.user, ))
        logger.info('Retrieving customer info (customer id: %s) ...' % (pk, ))

        queryset = [customer for customer in self.blacklist if customer.pk == int(pk)]
        serializer = serializers.CustomerSerializer(queryset, many=True, 
                context={'request':request})
        return Response(serializer.data, status=200)

    def destroy(self, request, pk=None):
        logger.info('Delete API')
        logger.info('User: %s' % (request.user, ))
        logger.info('Updating customer status (customer id: %s) ...' % (pk, ))
        models.Customer.objects.filter(pk=pk).update(status=models.Customer.STATUS_DELETED,
                deleted_by=request.user)

        logger.info('Deleting blacklist from memcached ...')
        cache.delete('blacklist')

        return Response(status=204)


class ListUsers(APIView):
    def get(self, request, format=None):
        """
        Return a list of all users.
        """

        queryset = models.Customer.objects.filter(status=models.Customer.STATUS_ACTIVE)
        serializer = serializers.CustomerSerializer(queryset, many=True)

        response = {
            'response': {
                'status': True,
                'results': serializer.data
            }
        }
        return Response(response)
