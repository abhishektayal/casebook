#import cass
import re
import time
from threading import Thread
from Queue import Queue
from urllib import urlopen

q = Queue()
workers = []
dict_photo_url={}
FILE = urlopen('http://enl.usc.edu/~cs694/casebook/config.txt').read()
def user_frnd_post(name):
    #print "in function"
    file = open(FILE, 'r')
    for line in file:
        #print "line is:",line
        match = line.split(' ', 1) 
        print match[0],"------->",match[1]
        if match:
            if not match[0] in 'photo':
                #print"in not photo- extracted:",match[0]
                if match[0] in 'user':
                     #print "in user"
                     stat= {}
                     MATCH= match[1].split(' ',2)
                     password= MATCH[2].split('\n',1)
                     stat['actual_name']=MATCH[1][1:-1]
                     stat['password']=password[0][1:-1]
                     #print 'actual name is:',MATCH[1]
                     #print 'password is:',password[0][1:-1]
                     #print 'user name is:',MATCH[0]
                     #cass.save_user(MATCH[0],stat)
                if match[0] in 'wallpost':     
                    stat1 ={}
                    #print 'in wallpost(), val is ',val
                    MATCH= match[1].split(' ',1)
                    #print 'user is',MATCH[0]
                    post= MATCH[1].split('\n',1)
                    stat1['body']=post[0][1:-1]
                    #print 'body is:',stat1['body']
                    #cass.save_post(MATCH[0],stat1)
                    
                else:
                    MATCH= match[0].split(' ',1)
                    #cass.add_friend(match[0],match[1][0:-1])     
                    
def downloader(worker_number):
        url = q.get()
        print q.qsize()
        data = urlopen(url).read()
        data_uri = data.encode("base64").replace("\n", "")
        dict_photo_url[url]=data_uri
        print "I am worker ",worker_number,"- downloaded image from url :",url
        #print"data is :",dict_photo_url[url]        
        q.task_done()

def photo_main(name):
    
    
    file = open(FILE, 'r')
    file2 = open(FILE, 'r')
    #print 'in photo()'
    for line in file:
        #print "line is:",line
        match = line.split(' ', 1)
        if match[0] in 'photo': 
            MATCH= match[1].split(' ',1)
            photo_url=MATCH[1].split('\n',1)
            #print "url is:",photo_url[0]
            
            if photo_url[0] in dict_photo_url.keys():
               # print"found url in dict no need to download"
                continue
            else:
                dict_photo_url[photo_url[0]]='url'
                #print"sending to worker"
                q.put(photo_url[0])
    #q.join()  
    #print "before going in................."          
    for line in file2:
           match = line.split(' ', 1)
           #print "For main aa gaya....."
           if match[0] in 'photo': 
            #print "Aaja mamu....."
            MATCH= match[1].split(' ',1)
            photo_url=MATCH[1].split('\n',1)
            #print 'url is:',MATCH[0], dict_photo_url[photo_url[0]]
            #cass.save_photo(MATCH[0], dict_photo_url[photo_url[0]] )
    
 
def main():
    print time.asctime()
    
    
    
    t1=Thread(target=user_frnd_post,args=("thread 1",))
    t2=Thread(target=photo_main,args=("thread 2",))
   
    
    
    print"there!!!!!!!!!!"    
    t1.start()
    t2.start()    
    #print dict_photo_url.keys()
    #user_frnd_post(f) 
    print"i am here"              
    t1.join()
    t2.join()
    q.join()
    print time.asctime()
    
      
               
if __name__ == "__main__":
    main()
