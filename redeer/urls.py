from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('redeer.gui.urls')),
    url(r'^api/', include('redeer.api.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

# Serve static files when debug false
if not settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT}),
        )
