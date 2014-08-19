import os.path
from django.conf.urls import patterns, include, url

from django.contrib import admin
from ota.views import *

admin.autodiscover()

site_media = os.path.join(
    os.path.dirname(__file__), 'site_media'
)

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index),
    url(r'^user/(\w+)/$', user),
    url(r'login/$', 'django.contrib.auth.views.login'),
    url(r'logout/$', logout_page),
    url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': site_media}),
    url(r'^register/$', register_page),
    url(r'^roms/new/$', addrom),
    url(r'^roms/(?P<id>\w+)/edit/$', editrom),
    url(r'^roms/(?P<id>\w+)/delete/$', deleterom),
    url(
        r'^rom/device=(?P<device>\w+)&rom=(?P<ota_id>\w+)&current_version=(?P<version>\d+)/$',
        query_update
    ),
)
