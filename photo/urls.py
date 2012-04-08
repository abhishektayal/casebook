from django.conf.urls.defaults import patterns, url
from users.views import login

urlpatterns = patterns('photo.views',
    url(r'^$', 'album', name='album'),
    
)
