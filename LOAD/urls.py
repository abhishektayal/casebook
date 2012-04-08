from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('LOAD.views',
    url('^/?$', 'load', name='load'),
    
)
