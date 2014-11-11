from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest_framework import routers

from core import views


router = routers.DefaultRouter()
router.register(r'customers', views.CustomerAPISet, 'customer')

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
