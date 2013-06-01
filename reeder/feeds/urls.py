from django.conf.urls import patterns, url

urlpatterns = patterns('reeder.feeds.views',
    # Examples:
    url(r'^upload/$', 'upload', name='upload'),
    url(r'^upload-succes/$', 'upload_success', name='upload-succes'),
)
