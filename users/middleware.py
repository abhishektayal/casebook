import cass

def get_user(request):
    if 'username' in request.session:
        try:
            '''
            passwd = cass.get_passwd(request.session['username'])
            #user=request.session['username']
            request.session['username']['is_authenticated'] = True
            return passwd
            '''
            user = cass.get_user_by_username(request.session['username'])
            passwd = cass.get_passwd(request.session['username'])
            user['passwd']=passwd
            
            return user
        except cass.DatabaseError:
            pass
    return {
        'password': None, 
        'is_authenticated': False,       
    }

class LazyUser(object):
    def __get__(self, request, obj_type=None):
        if not hasattr(request, '_cached_user'):
            request._cached_user = get_user(request)
        return request._cached_user

class UserMiddleware(object):
    def process_request(self, request):
        request.__class__.user = LazyUser()
