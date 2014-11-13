from django.conf.urls import patterns, url

from core import views


urlpatterns = patterns(
    '',
    url(
        r'^customers/?$',
        views.CustomerListCreateView.as_view(),
        name='customer-list'
    ),
    url(
        r'^customers/(?P<msisdn>\d+)/?',
        views.CustomerRetrieveDestroyView.as_view(),
        name='customer-detail'
    ),
)
