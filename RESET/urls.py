from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('RESET.views',
    url('^/?$', 'reset', name='reset'),
    
)
