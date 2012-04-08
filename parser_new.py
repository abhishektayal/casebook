#import cass
import re
import Pyro4
import time
from threading import Thread
from Queue import Queue
from urllib import urlopen
import urllib
import string
import re
import client
import subprocess


#from django.core.cache import cache


 
q = Queue()
workers = []
postQ=Queue()
POSTQ=Queue()
POST_SEARCH_INDEX={}
POST_SEARCH_INDEX1={}
FINAL_INDEX={}
stop_words_list=[]
GLOBAL_COUNTER=1
GLOBAL_COUNTER1=1
global_history=[]
global_history1=[]
TOTAL_WORDS=0





def user_frnd(name):
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
                    #cass.save_user(USER_PASS)
                    #cass.add_friend(USER_FRND)
                    break

    
   
    
    
    
    
def post(name): 
    
    print "in post ........"
    #file = open('conf.txt', 'r')
    file = open('file.txt', 'r',5000)
    print "read 5000 line in to the momeory from file.txt........"
    WALLPOST={}
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
                
                
                
                count=count+1
                ##print 'post, usr is:',MATCH[0]
                if count == 5000:                    
                    count=0
                    client.placework(LINE_NUMBER-5000, 5000)
                    #WALLPOST.clear()
         
    client.placework(LINE_NUMBER-count, count)                
    user_frnd(1)
    #cass.save_post(WALLPOST)                  
    
                  
                    
def downloader(photo_urls):
    for url in photo_urls.keys():
        filename = 'media/photos/'+photo_urls[url]
        file = open(filename, 'w')
        file.write(urlopen(url).read())
        file.close()


def photo_main(name):
    file = open('file.txt', 'r')
    CF_Photo={}
    photo_urls={}
    key_counter = 0
    for line in file:
        keyword = line.split(' ', 1)
        if keyword[0] in 'photo':
            user= keyword[1].split(' ',1)
            photo_url=user[1].split('\n',1)
            key_counter = key_counter +1
            URI = photo_url[0].split('/',6)
            CF_Photo[str(key_counter)] = {}
            CF_Photo[str(key_counter)]['userid']=user[0]
            CF_Photo[str(key_counter)]['URI']=URI[6]
            #check if the photo is already downloaded if not schedule for download                
            if photo_url[0] not in photo_urls.keys():
                photo_urls[photo_url[0]]=URI[6]
    #cass.save_photo(CF_Photo)            
    downloader(photo_urls)            



def remove_stop_words(word_list):
     
    
    
    without_stop_words=[]
    
   
    for word in word_list:
        #print word
        #print word
        
        if word not in stop_words_list:
            #print word
            without_stop_words.append(word)
            
            #print word
            
    #print without_stop_words
        #new_string = string.split(new_string)
        #line_stop_words = line_stop_words + [new_string]
    return(without_stop_words)
    
    
    
    
def RemovePunc(recv_line):
    line = []
    i = 0
    
    
    out = recv_line.translate(string.maketrans("",""), NEW)
    new_char_string=out.lower()
    broken_line=re.findall(r'\w+', new_char_string)
    #print broken_line
    #print recv_line
      
    return broken_line


def update_index(line,postid):
    global TOTAL_WORDS
    global POST_SEARCH_INDEX
    global GLOBAL_COUNTER
    global global_history
    """
    word_user_tuple=()
    global POST_SEARCH_INDEX
    global global_history
    for word in line:
        word_user_tuple=(word,user)
        if word not in global_history:   
            TOTAL_WORDS= TOTAL_WORDS+1         
            global_history.append(word)
            POST_SEARCH_INDEX[word]={}
        if  word_user_tuple not in global_history:
            global_history.append(word_user_tuple)   
            POST_SEARCH_INDEX[word][user]=[]
            
            
        POST_SEARCH_INDEX[word][user].append(postid)
    """
    GLOBAL_COUNTER= GLOBAL_COUNTER + 1
    for word in line:
        if word not in stop_words_list:
            if word not in global_history:
                 TOTAL_WORDS= TOTAL_WORDS+1         
                 global_history.append(word)
                 POST_SEARCH_INDEX[word]=set()
            
            POST_SEARCH_INDEX[word].add(int(postid))    
    
    
def update_index1(line,postid):
    global TOTAL_WORDS
    global POST_SEARCH_INDEX1
    global GLOBAL_COUNTER
    global global_history1
    global global_history
    """
    word_user_tuple=()
    global POST_SEARCH_INDEX
    global global_history
    for word in line:
        word_user_tuple=(word,user)
        if word not in global_history:   
            TOTAL_WORDS= TOTAL_WORDS+1         
            global_history.append(word)
            POST_SEARCH_INDEX[word]={}
        if  word_user_tuple not in global_history:
            global_history.append(word_user_tuple)   
            POST_SEARCH_INDEX[word][user]=[]
            
            
        POST_SEARCH_INDEX[word][user].append(postid)
    """
    GLOBAL_COUNTER= GLOBAL_COUNTER + 1
    for word in line:
        if word not in stop_words_list:
            if word not in global_history1:
                 if word not in global_history:
                     TOTAL_WORDS= TOTAL_WORDS+1         
                 global_history1.append(word)
                 POST_SEARCH_INDEX1[word]=set()
            
            POST_SEARCH_INDEX1[word].add(int(postid))    
       
def combine():
    
    print "inside merge",time.asctime()
    A = set(POST_SEARCH_INDEX.keys())  
    B= set(POST_SEARCH_INDEX1.keys())
    D= A.union(B)
    C= A.intersection(B)
    diffA= set(A.difference(C))
    diffB= set(B.difference(C))
    FINAL={}
    for keys in C:
        FINAL[keys]=POST_SEARCH_INDEX[keys].union(POST_SEARCH_INDEX1[keys])
    for keys in diffA:
        FINAL[keys]= POST_SEARCH_INDEX[keys]        
    for keys in diffB:
        FINAL[keys]= POST_SEARCH_INDEX1[keys]            
    POST_SEARCH_INDEX.clear()
    POST_SEARCH_INDEX1.clear()                
    print "done merge",time.asctime()
    print "no of keys are",(set(FINAL.keys())).__len__()
    
    

def main():
    print time.asctime()
    

    
    
    u = urllib.urlretrieve('http://enl.usc.edu/~cs694/casebook/config70.txt',"file.txt")
           
    #user_frnd(1)
    post(1)
    #combine()
    #photo_main(1)
    
    
    
    #t1=Thread(target=post,args=("thread 1",))
    #t2=Thread(target=photo_main,args=("thread 2",))
    #t3=Thread(target=downloader,args=("thread 3",))
    #t4=Thread(target=writer,args=("thread 4",))
    
   
    #t7.start()
    #t1.join()
    
    print time.asctime()
    return
      
      
      


            
      
      
               
if __name__ == "__main__":
    main()
