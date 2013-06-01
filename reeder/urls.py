from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^api/', include('reeder.api.urls')),
    url(r'^feeds/', include('reeder.feeds.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
