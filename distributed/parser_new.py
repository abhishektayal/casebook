import CASS
import Pyro4
import time
from urllib import urlopen
import urllib
import string
import client
import os


#from django.core.cache import cache


POST_SEARCH_INDEX={}
FINAL_INDEX={}
stop_words_list=[]
global_history=[]

TOTAL_WORDS=0
global WALLPOST
WALLPOST={}
global USER_POST
USER_POST={}

def user_frnd(name):
    global dispatcher
    #####print "in function"
    #file = open('conf.txt', 'r')
    file = open('file.txt', 'r',500)
    USER_PASS={}
    USER_FRND={}
    #file = open('conf.txt', 'r')
    ctr=0
    for line in file:
        ######print "line is:",line
        match = line.split(' ', 1) 
        #####print match[0],"------->",match[1]
        if match:
           
                #####print"in not photo- extracted:",match[0]
                if match[0] in 'user':
                     #####print "in user"
                     
                     MATCH= match[1].split(' ',1)
                     NEW=MATCH[1].split('"',4)
                     
                     USER_PASS[MATCH[0]]={} 
                     USER_FRND[MATCH[0]]={}
                     #####print NEW
                     
                     password= NEW[3]
                     USER_PASS[MATCH[0]]['actual_name']=NEW[1]
                     USER_PASS[MATCH[0]]['password']=password
                     #####print 'actual name is:',NEW[1]
                     #####print 'password is:',password
                     ##print 'user name is:',MATCH[0],'password is:',password
                     #cass.save_user(MATCH[0],stat)
                elif match[0] in 'friend':
                    ##print "line in frnd is",line
                    MATCH= match[1].split(' ',1)
                    ###print "frnds are",MATCH[0],MATCH[1][0:-1]
                    USER_FRND[MATCH[0]]['f'+str(ctr)]=MATCH[1][0:-1]
                    ctr=ctr+1
                    USER_FRND[MATCH[1][0:-1]]['f'+str(ctr)]= MATCH[0]
                    ctr=ctr+1
                    #cass.add_friend(MATCH[0],MATCH[1][0:-1])                   
                else:
                    print"inserting USER and FRIEND into cassandra ",time.asctime()
                    CASS.save_user(USER_PASS)
                    CASS.add_friend(USER_FRND)
                    dispatcher.store_user_count(len(USER_PASS.keys()))
                    break

    

def post(name): 
    global WALLPOST
    global USER_POST
    print "in post ........"
    #file = open('conf.txt', 'r')
    file = open('file.txt', 'r',5000)
    print "read 5000 line in to the momeory from file.txt........"#,time.asctime()    
    ctr=0
    count=0
    LINE_NUMBER=0
    for line in file:
        
        ctr=ctr+1
        LINE_NUMBER= LINE_NUMBER +1
        ######print "line is:",line
        match = line.split(' ', 1) 
        #####print match[0],"------->",match[1]
        
        if match[0] in 'wallpost':     
                WALLPOST[str(ctr)]={}
                #####print 'in wallpost(), val is ',val
                MATCH= match[1].split(' ',1)
                #####print 'user is',MATCH[0]
                post= MATCH[1].split('\n',1)
                WALLPOST[str(ctr)]['body']=post[0][1:-1]
                WALLPOST[str(ctr)]['userid']=MATCH[0]
                
                if MATCH[0] not in USER_POST.keys():
                    USER_POST[MATCH[0]]={}
                    USER_POST[MATCH[0]]['postid_set']=str()
                    
                USER_POST[MATCH[0]]['postid_set']+=','+(str(ctr))
                
                count=count+1
                ##print 'post, usr is:',MATCH[0]
                if count == 5000:                    
                    count=0
                    client.placework(dispatcher,LINE_NUMBER-5000, 5000)
                    #WALLPOST.clear()
         
    if count>0:
        client.placework(dispatcher,LINE_NUMBER-count, count)                
    

    

def main():
    global WALLPOST
    global USER_POST
    global dispatcher
    print "START______________________",time.asctime()

    
    # reset dispatcher and wait for reply
    print "resetting dispatcher"
    dispatcher = Pyro4.core.Proxy("PYRONAME:example.distributed.dispatcher")
    async2=Pyro4.async(dispatcher)
    async2_result= async2.reset()
    
    print "killing the worker on my machine"
    os.system("kill -9 `ps -eaf | grep -i worke[r] | awk '{print $2}'`")
    
    print "start download for self",time.asctime()
    u = urllib.urlretrieve('http://enl.usc.edu/~cs694/casebook/config70.txt',"file.txt")
    print "downloaded file",time.asctime()   
    
    #sending trigger to photo server1
    photo_client=Pyro4.Proxy("PYRONAME:photo.async")
    photo_async=Pyro4.async(photo_client)
    photo_result1=photo_async.process_photo("http://enl.usc.edu/~cs694/casebook/config20.txt")
    
    #sending trigger to photo server2
    photo_client2=Pyro4.Proxy("PYRONAME:photo.async2")
    photo_async2=Pyro4.async(photo_client2)
    photo_result2=photo_async2.process_photo("http://enl.usc.edu/~cs694/casebook/config20.txt")
    
    # trigger the downloaders asynchronously and do not wait for replies
    print "sending to downloader1"
    download_daemon=Pyro4.Proxy("PYRONAME:download_daemon")
    #download_daemon.download('http://enl.usc.edu/~cs694/casebook/config70.txt',"file.txt")
    async1=Pyro4.async(download_daemon)
    async1_result= async1.download('http://enl.usc.edu/~cs694/casebook/config20.txt')
    
    
    download_daemon1=Pyro4.Proxy("PYRONAME:download_daemon2")
    print "sending to downloader2"
    #download_daemon.download('http://enl.usc.edu/~cs694/casebook/config70.txt',"file.txt")
    async3=Pyro4.async(download_daemon1)
    async3_result= async3.download('http://enl.usc.edu/~cs694/casebook/config20.txt')
    
    
    # starting worker on my own machine
    print"starting worker on my node"
    os.system("python worker.py &")
    #os.system("python worker.py &")
    
    
    post(1)
    
    print "calling the aggregate function",time.asctime()
    async5=Pyro4.async(dispatcher)
    async5_result= async5.aggregate()
    
    
    
    photo_merge_done=0
    post_index_done=0
    while(1):
        if photo_merge_done==0:            
            if photo_result1.ready and photo_result2.ready:
                photo_merge_done=1
                merged={}
                result1 =  photo_result1.value
                result2 =  photo_result2.value
                print "photo Results received... Merging them"
                A = set(result1.keys())
                B = set(result2.keys())
                common = A.intersection(B)
                onlyA = set(A.difference(common))
                onlyB = set(B.difference(common))
                for keys in common:
                    merged[keys] = result1[keys].union(result2[keys])
                for keys in onlyA:
                    merged[keys] = result1[keys]
                for keys in onlyB:
                    merged[keys] = result2[keys]
                photo_index = {}
                for keys in merged:
                    photo_index[keys] = {}
                    photo_index[keys]['photoid']=','.join(merged[keys])
                CASS.save_photo(photo_index)    
                print"inserted photo  in cass"
                
        if post_index_done==0:                                    
            if async5_result.ready:
                post_index_done=1  
                user_frnd(1)
                
                print "inserting USER_POST in cassandra",time.asctime()
                CASS.save_WALL(USER_POST)
                print"inserting WALLPOST into cassandra ",time.asctime()
                length=len(WALLPOST.keys())
                PPP=0
                temp={}
                for keys in WALLPOST:
                    PPP=PPP+1
                    temp[keys]=WALLPOST[keys]
                    if PPP==500:
                        CASS.save_post(temp)
                        temp.clear()
                        PPP=0
                CASS.save_post(temp)
        
        if photo_merge_done==1 and post_index_done==1:
            break

        
            
        
    #post(1)
    print "DONE_____________________",time.asctime()
    return
      
      
      


            
      
      
               
if __name__ == "__main__":
    main()
