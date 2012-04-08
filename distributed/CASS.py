import time
import uuid
import pycassa
import base64
import random
import pycassa.pool
from pycassa.cassandra.ttypes import NotFoundException
from urllib import urlopen





#from multiprocessing.managers import dic

__all__ = ['get_user_by_username', 'get_friend_usernames',
    'get_follower_usernames', 'get_users_for_usernames', 'get_friends',
    'get_followers', 'get_timeline', 'get_userline', 'get_tweet', 'save_user',
    'save_tweet', 'add_friends', 'remove_friends', 'DatabaseError',
    'NotFound', 'InvalidDictionary', 'PUBLIC_USERLINE_KEY']


POOL = pycassa.pool.ConnectionPool('Casebook_test', server_list=['10.0.2.3:9160','10.0.2.4:9160'],timeout=None,pool_size=2,prefill=False)
#POOL_DUMMY=POOL
#POOL=pycassa.connect('Casebook_test',['10.0.2.3:9160','10.0.2.5:9160','10.0.2.6:9160','10.0.2.7:9160','10.0.2.8:9160'])

USER = pycassa.ColumnFamily(POOL, 'User')
FRIENDS = pycassa.ColumnFamily(POOL, 'Friends')

PHOTO_ALBUM = pycassa.ColumnFamily(POOL, 'Photo_Album')

WALL = pycassa.ColumnFamily(POOL, 'Wall')
POST = pycassa.ColumnFamily(POOL, 'Post')
PHOTO_STORE = pycassa.ColumnFamily(POOL, 'Photo_store')
PHOTO = pycassa.ColumnFamily(POOL, 'Photo')
#global dictonary for saved photo url
dict_photo_url = {}

# NOTE: Having a single userline key to store all of the public tweets is not
#       scalable.  Currently, Cassandra requires that an entire row (meaning
#       every column under a given key) to be able to fit in memory.  You can
#       imagine that after a while, the entire public timeline would exceed
#       available memory.
#
#       The fix for this is to partition the timeline by time, so we could use
#       a key like !PUBLIC!2010-04-01 to partition it per day.  We could drill
#       down even further into hourly keys, etc.  Since this is a demonstration
#       and that would add quite a bit of extra code, this excercise is left to
#       the reader.
PUBLIC_USERLINE_KEY = '!PUBLIC!'


class DatabaseError(Exception):
    """
    The base error that functions in this module will raise when things go
    wrong.
    """
    pass


class NotFound(DatabaseError):
    pass


class InvalidDictionary(DatabaseError):
    pass

def reset_keyspace():
     POST.truncate()
     PHOTO_ALBUM.truncate()

def get_user_by_username(userid):
    return userid

def get_friend( username):
    """
    Gets the social graph (friends or followers) for a username.
    """
    try:
        friends = FRIENDS.get(str(username))
        ###print friends.values()
    except NotFoundException:
        return []
    return friends.values()


def get_wall(userid, limit):
    """
    Gets a wall posts for a user, a start, and a limit.
    """
    # First we need to get the list of post ids for a given userid from its wall
    ######print"got - ",userid
    start = ''
    limit = long(limit)
    next = None
    try:
	#Get all post from users wall
        timeline = WALL.get(str(userid), column_start=start,
            column_count=limit, column_reversed=True)
    except NotFoundException:
        return [], next

    if len(timeline) == limit:
        next = long(limit)+ 100
    else:
        next = None
    ####print "first post id list is :",timeline
    # Now we do a multiget to get the posts with userid
    post_ids = timeline.values()
    ####print"post ids are:",post_ids
    wall_dict = POST.multiget(post_ids) 
    
    
    ####print"wall dict are:",wall_dict
    list=[]
    new_wall_dict={}
    keys=['userid','type','body']
    values=[]
    for id, dict in wall_dict.iteritems():
        
        if dict['type']=='0':
                
                list.append(dict)
        else:
            ######print "id is -------------",id
            values.insert(0, dict['userid'])  
            values.insert(1,1)
            values.insert(2,PHOTO_STORE.get(dict['body'])['data'])
            list.append(zip(keys,values))
            ####print "in retrieving post",new_wall_dict
            
    ##print list
    return (list, next)
       
    


# QUERYING APIs

def get_passwd(userid):
    """
    Given a userid, return his password.
    """
    try:
        user = USER.get(str(userid))
    except NotFoundException:
        raise NotFound('User %s not found' % (userid))
    return user['password']


def get_photos(userid, limit):
    """
    Gets photos for a user, a start, and a limit.
    """
    # First we need to get the list of photo ids for a given userid
    ######print"got - ",userid
    start = ''
    limit = long(limit)     
    next = None
    try:
	#Get all post from users wall
        timeline = PHOTO_ALBUM.get(str(userid), column_start=start,
            column_count=limit, column_reversed=True)
    except NotFoundException:
        return [], next
    ##print "in get 1-",timeline
    if len(timeline) == limit:
        next = long(limit)+ 100
    else:
        next = None    
        
    # Now we do a multiget to get the photos with photoid
    photo_ids = timeline.values()
    ##print "in get 2-",photo_ids
    #####print "then it extracts:",photo_ids
    ######print "timeline values are:",photo_ids
    photo_urls = POST.multiget(photo_ids)
    
    #####print "-------------",photo_urls
    list=[]
    new_photo_dict={}
    keys=['userid','type','body']
    values=[]
    #for key in photo_urls.keys():
    #   ##print "in get 3",photo_urls[key]
    for id, dict in photo_urls.iteritems():
        #values.insert(0, dict['userid'])  
        #values.insert(1,1)
        #values.insert(2,PHOTO_STORE.get(dict['body'])['data'])
        list.append(PHOTO_STORE.get(dict['body'])['data'])
        
        ##print "total list is",list
        
    return (list, next)

# INSERTING APIs

def save_user(user_dict):
    """
    Saves the user record.
    """
    USER.batch_insert(user_dict)
    
def save_WALL(wall_dict):    
    WALL.batch_insert(wall_dict)

def save_post( post_details):
    """
    Saves the tweet record. The record send will be a dic with body:msg.
    """
    """
    # Generate a timestamp for the USER/TIMELINE
    ts = str(long(time.time() * 1e6))
    post_id = str(uuid.uuid1())
    # Make sure the post msg  body is utf-8 encoded
    #post['body'] = post['body'].encode('utf-8')
    #post['body'] = post['body']
    #post['userid'] = 
    post['type'] = '0'
    # Insert the post, then into the user's wall, then into user's friends wall
    POST.insert(str(post_id), post)
        
    # Get the user's friends, and insert the post into all of their walls
    friends_ids = [post['userid']] + get_friend(post['userid'])
    for friends in friends_ids:
        WALL.insert(str(friends), {ts: str(post_id)})
        """
    POST.batch_insert(post_details)    

def save_photo(photo_details):
    """
    Saves the tweet record. The record send will be a dic with body:msg.
    """
    # Generate a timestamp for the USER/TIMELINE
    PHOTO.batch_insert(photo_details)

def add_friend(friend_details):
    """
    Adds a friendship relationship from one user to some others.
    """
    ###print "frnds passed are",userid,friend
    
    
    # friendship is two way. Add yourself as a friend to him as well
    FRIENDS.batch_insert(friend_details)
 
"""   
def add_multiple_friends(userid, friend_ids):
   
    ts = str(int(time.time() * 1e6))
    dct = pycassa.util.OrderedDict(((str(username), ts) for username in to_usernames))
    FRIENDS.insert(str(from_username), dct)
    for to_username in to_usernames:
        FOLLOWERS.insert(str(to_username), {str(from_username): ts})
"""

def main():
    save_photo('user1', 'xyz', 'http://enl.usc.edu/~cs694/casebook/photos/photo73.jpg')
    save_photo('user1', 'qweqeeqweqw', 'http://enl.usc.edu/~cs694/casebook/photos/photo72.jpg')
    post1={}
    post2={}
    post1['body']='post1 -----'
    post2['body']='post2 -----'
    save_post('user1', post1)
    save_post('user1', post2)
    get_photos('user1', 4)
    #get_photos('user2', 1)
    
    
    
if __name__ == "__main__":
    main()
	
    
