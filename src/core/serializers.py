from rest_framework import serializers, pagination

from core import models


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    created_by = serializers.RelatedField()

    class Meta:
        model = models.Customer
        fields = ('id', 'url', 'msisdn', 'date_inserted', 'created_by')
        lookup_field = 'msisdn'


class PaginatedCustomerSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class = CustomerSerializer
