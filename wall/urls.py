from django.conf.urls.defaults import patterns, url,include
from users.views import login

urlpatterns = patterns('wall.views',
    #url(r'^login/$', 'login', name='login')
    #url(r'^/?$', 'timeline', name='timeline'),
    #url(r'^public/$', 'publicline', name='publicline'),
    #url(r'^(?P<username>\w+)/$', 'userline', name='userline'),
    #url(r'^/?$', 'userline', name='userline'),
    url('', 'userline',name='user'),
)
    #url(r'^?user=$(?P<user>\w{4}\d{1,2,3})&/type=(?P<type>\w{4,5})&/scope=(?P<scope>\w{4})&/terms=(?P<terms>(\w\+)+)$', 'userline',name='user'),
#(?P<user>\w{4}\d{1,2,3})&/type=(?P<type>\w{4,5})&/scope=(?P<scope>\w{4})&/terms=(?P<terms>\w+)$


#http://<home>/SEARCH?user=<u>&type=<t>&scope=<s>&terms=<tm>