from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('redeer.gui.urls')),
    url(r'^api/', include('redeer.api.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
