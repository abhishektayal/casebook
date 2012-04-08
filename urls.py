from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    url('login', include('users.urls')),
    url('^auth/', include('users.urls')),
    url('^wall/$', include('wall.urls')),
    url('^photo/$', include('photo.urls')),
    url('^LOAD/$', include('LOAD.urls')),
    url('^RESET/$', include('RESET.urls')),
    url('^SEARCH/$', include('wall.urls')),
      
)

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'^media/(?P<path>.*)$', 'serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )



#http://<home>/SEARCH?user=<u>&type=<t>&scope=<s>&terms=<tm>