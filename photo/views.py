import uuid

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse

from wall.forms import WallForm

import cass

NUM_PER_PAGE = 20



def album(request):
    username = request.session['username']
    menu=1
    try:
        passwd = cass.get_passwd(username)
    except cass.DatabaseError:
        raise Http404
    """
    # Query for the friend ids
    friend_usernames = []
    friend_usernames = cass.get_friend(username) + [username]
    
    # Add a property on the user to indicate whether the currently logged-in
    # user is friends with the user
    user['friend'] = username in friend_usernames
    """
    
    limit = request.GET.get('start')
    if not limit:
        limit='20'
    photos,next = cass.get_photos(username, limit=limit)
    context = {
        'user': username,
        'username': username,
        'photos': photos,
        'next': next,
        'menu':menu,
        
    }
    
    return render_to_response('photo/album.html', context,
        context_instance=RequestContext(request))


	
