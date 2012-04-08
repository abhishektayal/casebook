from __future__ import print_function

try:
    import queue
except ImportError:
    import Queue as queue
import Pyro4
import time
from workitem import Workitem

class DispatcherQueue(object):
    def __init__(self):
        self.workqueue = queue.Queue()
        self.resultqueue = queue.Queue()
        self.final_index={}
        self.total_work_objects=0
        self.TOTAL_USERS=0
    def putWork(self, item):
        
        self.total_work_objects= self.total_work_objects +1
        print ("got work, total objects got= ->",self.total_work_objects)
        self.workqueue.put(item)
    def getWork(self, timeout=10):
        return self.workqueue.get(block=True, timeout=timeout)
    def putResult(self, item):
        print ("now inserting result received , Q size is->",self.resultqueue.qsize())
        self.resultqueue.put(item)
        print ("result got , Q size is->",self.resultqueue.qsize())
    def getResult(self, timeout=10):
        return self.resultqueue.get(block=True, timeout=timeout)
    def workQueueSize(self):
        return self.workqueue.qsize()
    def resultQueueSize(self):
        return self.resultqueue.qsize()
    def reset(self):
        print ("resetting self")
        self.workqueue = queue.Queue()
        self.resultqueue = queue.Queue()
        self.final_index={}
        self.total_work_objects=0
        self.TOTAL_USERS=0
    def aggregate(self):            
        print ("aggregate called, waiting for all responses",time.asctime())
        while self.resultqueue.qsize() != self.total_work_objects:
            #print ("in while ------------result Q size is",self.resultqueue.qsize()," waiting for",self.total_work_objects)
            #time.sleep(3)
            continue
        print ("starting to aggregate.....",time.asctime())
        if self.total_work_objects ==  1:
          temp = (self.resultqueue.get()).result  
          for key in temp.keys():
             self.final_index[key] = temp[key]
          return 1
        
        dict_obj2 = (self.resultqueue.get()).result        
        dict_obj3 = (self.resultqueue.get()).result
          
        SET_A= set(dict_obj2.keys())
        SET_B= set(dict_obj3.keys())
        
        intersection= SET_A.intersection(SET_B)
        diffA= SET_A.difference(intersection)
        diffB=SET_B.difference(intersection)
        for key in intersection:
            self.final_index[key]= dict_obj2[key].union(dict_obj3[key])
        for key in diffA:
            self.final_index[key]=dict_obj2[key]
        for key in diffB:
            self.final_index[key]=dict_obj3[key]    
        
        
        #print("result after aggregation part -1 is :",self.final_index)
        #print ("q left is:",self.resultqueue.qsize())
        for each_item in range(0,self.resultqueue.qsize()):
            
            dict_obj3 = (self.resultqueue.get()).result     
            SET_A= set(dict_obj3.keys())
            SET_B= set(self.final_index.keys())
            
            intersection= SET_A.intersection(SET_B)
            diffA= SET_A.difference(intersection)
            for key in intersection:
                self.final_index[key]= dict_obj3[key].union(self.final_index[key])
            for key in diffA:
                self.final_index[key]=dict_obj3[key]
             
        print ("done  aggregating .......",time.asctime())
        print("totalwords in the final index are .....",len(self.final_index.keys()))
        
        return 1 

    def store_user_count(self,count):  
        print ("saved total no of users=",count)   
        self.TOTAL_USERS=count
        return
    def get_user_count(self):
        print("returned total no of users=",self.TOTAL_USERS)
        return self.TOTAL_USERS
    def get_post_ids(self,WORD_list):    
        print("in get post_ids")
        return_postid_list=[]
        return_postid_set=set()
        print ("looking for words->",WORD_list)
        for word in WORD_list:
            
            
            #return_postid_set.add(self.final_index[word])
            if word in self.final_index.keys():
                print("index set is:",self.final_index[word])
                return_postid_set=return_postid_set.union(self.final_index[word])
        #if len(return_postid_list)== 0:
	    #return_postid_list.append(set())   
        return_postid_list.append(return_postid_set)
        #print (return_postid_list)
        print (return_postid_list)
        return return_postid_list        
     
    
        
        
        
######## main program

ns=Pyro4.naming.locateNS()
Pyro4.config.HOST="10.0.2.3"
daemon=Pyro4.core.Daemon()
dispatcher=DispatcherQueue()
uri=daemon.register(dispatcher)
ns.register("example.distributed.dispatcher", uri)
print("Dispatcher is ready.")


daemon.requestLoop()
    
