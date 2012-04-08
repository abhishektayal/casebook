from __future__ import print_function
import os,socket,sys,string
from math import sqrt
import time
import re
try:
    import queue
except ImportError:
    import Queue as queue
import Pyro4
from workitem import Workitem

if sys.version_info<(3,0):
    range=xrange
import workitem


WORKERNAME = "Worker_%d@%s" % (os.getpid(), socket.gethostname())
#global TOTAL_WORDS
global LINES
LINES=[]
file = open('file.txt', 'r')
LINES=file.readlines()
global NEW
NEW=string.punctuation + '0123456789'
global global_history_total
global_history_total=[]

def RemovePunc(recv_line):
    line = []
    i = 0
    
    global NEW
    out = recv_line.translate(string.maketrans("",""), NEW)
    new_char_string=out.lower()
    broken_line=re.findall(r'\w+', new_char_string)
    #print broken_line
    #print recv_line
      
    return broken_line



def update_index(line,user,postid):
    
    global POST_SEARCH_INDEX
    global stop_words_list
    global global_history
    #global TOTAL_WORDS
    
    for word in line:
        #post_key=user+':'+word
        if word not in stop_words_list:
            if word not in global_history:
                 
                 global_history.append(word)
                 POST_SEARCH_INDEX[word]=set()
            
            POST_SEARCH_INDEX[word].add(int(postid)) 
            #print ("updated index -> ",POST_SEARCH_INDEX[word])


def indexing_range(start,total):
    global LINES
    for line_no in range(start,start+total):
        PUNC_REMOVED=[]
        line=LINES.__getitem__(line_no)
        #print ("line is ->",line)
        
        ######print "line is:",line
        match = line.split(' ', 2) 
        #####print match[0],"------->",match[1]

        #####print 'in wallpost(), val is ',val
        USER=match[1]
        #print(" user is ",USER)
        #####print 'user is',MATCH[0]
        dummy_post= match[2].split('\n',1)
        POST=dummy_post[0][1:-1]
        #print(" post is ",POST)
        
        #indexing functions
        no_punc_upper=[]
        no_punc_upper= RemovePunc(POST)
        #print (" no punc is ",no_punc_upper)
        update_index(no_punc_upper,USER,str(line_no))
        
        





def process(item):
    #print("factorizing %s -->" % item.data)
    #sys.stdout.flush()
    global POST_SEARCH_INDEX,global_history
    POST_SEARCH_INDEX={}
    global_history=[]
    
    indexing_range(item.start,item.total)
    item.result=POST_SEARCH_INDEX
    #print(item.result)
    item.processedBy = WORKERNAME

def main():
    #global TOTAL_WORDS
    
    TOTAL_POSTS=0
    #TOTAL_WORDS=0
    TOTAL_IDLE=0
    global stop_words_list
    stop_words_file=open('stop_words.txt','r')
    for line in stop_words_file:
        stop_words_list= set(re.findall(r'\w+', line))
    stop_words_file.close()  
    
    #item=workitem.Workitem(10000,2)
    #process(item)
    
    
    dispatcher = Pyro4.core.Proxy("PYRONAME:example.distributed.dispatcher")
    print("This is worker %s" % WORKERNAME)
    print("getting work from dispatcher.")
    while True:
        try:
            item = dispatcher.getWork()
            TOTAL_POSTS=TOTAL_POSTS + item.total
        except queue.Empty:
            TOTAL_IDLE+= 1
            if TOTAL_POSTS > 0 or TOTAL_IDLE > 5:
                sys.exit()
            print("no work available yet.")
        else:
            print("got one item ->",time.asctime() )
            process(item)
            #print ("TOTAL WORDS INDEXED UPTIL NOW ->",TOTAL_WORDS, "total posts indexed ->",TOTAL_POSTS)
            dispatcher.putResult(item)
            print("returned one item ->",time.asctime() )

if __name__=="__main__":
    main()
