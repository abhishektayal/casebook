import uuid

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse

from wall.forms import WallForm

import cass

NUM_PER_PAGE = 200


def timeline(request):
    form = WallForm(request.POST or None)
    if request.user['is_authenticated'] and form.is_valid():
        tweet_id = str(uuid.uuid1())
        cass.save_tweet(tweet_id, request.session['username'], {
            'username': request.session['username'],
            'body': form.cleaned_data['body'],
        })
        return HttpResponseRedirect(reverse('timeline'))
    start = request.GET.get('start')
    if request.user['is_authenticated']:
        tweets,next = cass.get_timeline(request.session['username'],
            start=start, limit=NUM_PER_PAGE)
    else:
        tweets,next = cass.get_userline(cass.PUBLIC_USERLINE_KEY, start=start,
            limit=NUM_PER_PAGE)
    context = {
        'form': form,
        'tweets': tweets,
        'next': next,
    }
    return render_to_response('wall/timeline.html', context,
        context_instance=RequestContext(request))

def publicline(request):
    start = request.GET.get('start')
    tweets,next = cass.get_userline(cass.PUBLIC_USERLINE_KEY, start=start,
        limit=NUM_PER_PAGE)
    context = {
        'tweets': tweets,
        'next': next,
    }
    return render_to_response('wall/publicline.html', context,
        context_instance=RequestContext(request))
"""
def userline(request):
    username = request.session['username']
    menu=1
    try:
        passwd = cass.get_passwd(username)
    except cass.DatabaseError:
        raise Http404
    
    # Query for the friend ids
    friend_usernames = []
    friend_usernames = cass.get_friend(username) + [username]
    
    # Add a property on the user to indicate whether the currently logged-in
    # user is friends with the user
    user['friend'] = username in friend_usernames
    
    
    limit = request.GET.get('start')
    #print "got this from html:",limit
    if not limit:
        limit='200'
    
    posts,next = cass.get_wall(username, limit=limit)
    context = {
        'user': username,
        'username': username,
        'posts': posts,
        'next': next,
        'menu':menu
    }
    
    return render_to_response('wall/userline.html', context,
        context_instance=RequestContext(request))



  """          

def userline(request):
    #http://<home>/SEARCH?user=<u>&type=<t>&scope=<s>&terms=<tm>  scope=user, snet, or glob
    user= request.GET.get('user','')
    type=request.GET.get('type','')
    scope= request.GET.get('scope','')
    terms=request.GET.get('terms','')
    
    
    
    print user,type,scope,terms
    
    print "inside search query"
    photos=[]
    
    if type=='photo':
        if scope=='user':
            object_list=cass.query_photo_index_user(user,terms)
            
        elif scope=='snet':
            object_list=cass.query_photo_index_group(user,terms)
            
        elif scope=='glob':
            object_list=cass.query_photo_index_global(user,terms)
            
    
    elif type=='post':
        if scope=='user':
            object_list=cass.query_post_index_user(user,terms)
            
        elif scope=='snet':
            object_list=cass.query_post_index_group(user,terms)
            
        elif scope=='glob':
            object_list=cass.query_post_index_global(user,terms)
            

            
    context = {
            'user': user,
            'username':user,
            'posts': object_list,
            'type':type,
            #'next': next,
            'menu':menu
        }
        
    return render_to_response('wall/search.html', context,
            context_instance=RequestContext(request))
         
     

    
