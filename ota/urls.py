from django.conf.urls import *
from ota.views import index, user

urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^user/(\w+)/$', user),
)
