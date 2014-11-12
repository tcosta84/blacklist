from django.conf.urls import patterns, url

from core import views


urlpatterns = patterns(
    '',
    url(
        r'^customers/?$',
        views.CustomerListView.as_view(),
        name='customer-list'
    ),
    url(
        r'^customers/(?P<msisdn>\d+)/?',
        views.CustomerDetailView.as_view(),
        name='customer-detail'
    ),
)
