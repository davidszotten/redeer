from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^api/$', 'reeder.api.views.index', name='index'),
    url(r'^feeds/', include('reeder.feeds.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
