from django.conf.urls import patterns, url

urlpatterns = patterns('reeder.gui.views',
    url(r'^$', 'index', name='index'),
    url(r'^upload/$', 'upload', name='upload'),
    url(r'^upload-succes/$', 'upload_success', name='upload-succes'),
)
