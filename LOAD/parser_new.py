import CASS
import Pyro4
import time
from urllib import urlopen
import urllib
import string
#import client
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

class Workitem(object):
    def __init__(self, start, total):
        print("Created workitem %s" % start, total)
        self.start=start
        self.total=total
        self.result=None
        self.processedBy=None

def placework(dispatcher,start,total):
    
    print("placing work items into dispatcher queue.")
    
    item = Workitem(start, total)
    
    dispatcher.putWork(item)


def user_frnd(name):
    global dispatcher
    file = open('/home/ubuntu/casebook/LOAD/file.txt', 'r',500)
    USER_PASS={}
    USER_FRND={}
    ctr=0
    for line in file:
        match = line.split(' ', 1) 
        if match:
                if match[0] in 'user':
                     MATCH= match[1].split(' ',1)
                     NEW=MATCH[1].split('"',4)
                     USER_PASS[MATCH[0]]={} 
                     USER_FRND[MATCH[0]]={}
                     password= NEW[3]
                     USER_PASS[MATCH[0]]['actual_name']=NEW[1]
                     USER_PASS[MATCH[0]]['password']=password
                elif match[0] in 'friend':
                    MATCH= match[1].split(' ',1)
                    USER_FRND[MATCH[0]]['f'+str(ctr)]=MATCH[1][0:-1]
                    ctr=ctr+1
                    USER_FRND[MATCH[1][0:-1]]['f'+str(ctr)]= MATCH[0]
                    ctr=ctr+1
                else:
                    print"inserting USER and FRIEND into cassandra ",time.asctime()
                    CASS.save_user(USER_PASS)
                    CASS.add_friend(USER_FRND)
                    dispatcher.store_user_count(len(USER_PASS.keys()))
                    break

    

def post(name): 
    global WALLPOST
    global USER_POST
    file = open('/home/ubuntu/casebook/LOAD/file.txt', 'r',5000)
    print "read 5000 line in to the momeory from file.txt........"#,time.asctime()    
    ctr=0
    count=0
    LINE_NUMBER=0
    for line in file:
        LINE_NUMBER= LINE_NUMBER +1
        match = line.split(' ', 1) 
        if match[0] in 'wallpost':     
                WALLPOST[str(ctr)]={}
                MATCH= match[1].split(' ',1)
                post= MATCH[1].split('\n',1)
                WALLPOST[str(ctr)]['body']=post[0][1:-1]
                WALLPOST[str(ctr)]['userid']=MATCH[0]
                if MATCH[0] not in USER_POST.keys():
                    USER_POST[MATCH[0]]={}
                    USER_POST[MATCH[0]]['postid_set']=str()
                USER_POST[MATCH[0]]['postid_set']+=','+(str(ctr))
                count=count+1
                if count == 5000:                    
                    count=0
                    placework(dispatcher,LINE_NUMBER-5000, 5000)
        ctr=ctr+1
    if count>0:
        placework(dispatcher,LINE_NUMBER-count, count)                


def parse():
        photo_urls = {}
        #os.system("scp -i abhi.pem -q ubuntu@10.0.2.3:./casebook/LOAD/file.txt .")
        #urllib.urlretrieve(confurl, "file.txt")
        #Parse config file to get photo URL's
        file = open('/home/ubuntu/casebook/LOAD/file.txt', 'r',8096)
        ph_line = 0
        for line in file:
            if line.startswith('photo'):
                ph_line=1
                parts = line.strip().split(' ', 2)
                #check if the photo is already downloaded if not schedule for download                
                if parts[2] not in photo_urls.keys():
                    photo_urls[parts[2]]=[]
                    photo_urls[parts[2]].append(str(parts[1]))
                else:
                    photo_urls[parts[2]].append(str(parts[1]))
            else:
                if ph_line==1:
                    break
        return photo_urls

def combine(result1, result2):
    merged={}
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
    return merged 


def main():
    global WALLPOST
    global USER_POST
    global dispatcher
    print "START______________________",time.asctime()
    
    print "killing the worker on my machine"
    os.system("kill -9 `ps -eaf | grep -i worke[r] | awk '{print $2}'`")

    print "start download for self",time.asctime()
    u = urllib.urlretrieve('http://enl.usc.edu/~cs694/casebook/config.txt',"/home/ubuntu/casebook/LOAD/file.txt")
    print "downloaded file",time.asctime()   
    
    #Parsing and distributing photo's to processor's
    photo_urls = {}
    photo_urls = parse()
    total_photos = len(photo_urls.keys())
    #chunk_size = total_photos/3
    #split photo's in to 3 disparate sets.
    photo_url_1={}
    photo_url_2={} 
    photo_url_3={}
    shuffle=1
    for key in photo_urls:
        if shuffle == 1:
           photo_url_1[key] = []
           photo_url_1[key].extend(photo_urls[key])
           shuffle=2
           continue
        if shuffle == 2:
           photo_url_2[key] = []
           photo_url_2[key].extend(photo_urls[key])
           shuffle=3
           continue
        if shuffle == 3:
           photo_url_3[key] = []
           photo_url_3[key].extend(photo_urls[key])
           shuffle=1
           continue

    #sending trigger to photo server1
    photo_client=Pyro4.Proxy("PYRONAME:photo.async")
    photo_async=Pyro4.async(photo_client)
    photo_result1=photo_async.process_photo(photo_url_1)
    
    #sending trigger to photo server2
    photo_client2=Pyro4.Proxy("PYRONAME:photo.async2")
    photo_async2=Pyro4.async(photo_client2)
    photo_result2=photo_async2.process_photo(photo_url_2)
    
    #sending trigger to photo server3
    photo_client3=Pyro4.Proxy("PYRONAME:photo.async3")
    photo_async3=Pyro4.async(photo_client3)
    photo_result3=photo_async3.process_photo(photo_url_3)

    # trigger the downloaders asynchronously and do not wait for replies
    """
    print "sending to downloader1"
    download_daemon=Pyro4.Proxy("PYRONAME:download_daemon")
    #download_daemon.download('http://enl.usc.edu/~cs694/casebook/config5.txt',"file.txt")
    async1=Pyro4.async(download_daemon)
    async1_result= async1.download()
    """
    print "done all photo work- ",time.asctime()
    
    # reset dispatcher and wait for reply
    print "resetting dispatcher"
    dispatcher = Pyro4.core.Proxy("PYRONAME:example.distributed.dispatcher")
    async2=Pyro4.async(dispatcher)
    async2_result= async2.reset()
    download_daemon1=Pyro4.Proxy("PYRONAME:download_daemon2")

    print "sending to downloader2"
    #download_daemon.download('http://enl.usc.edu/~cs694/casebook/config70.txt',"file.txt")
    async3=Pyro4.async(download_daemon1)
    async3_result= async3.download()
    
    
    # starting worker on my own machine
    print"starting worker on my node"
    os.system("python /home/ubuntu/casebook/LOAD/worker.py &")
    #os.system("python worker.py &")
    
    #Parsing user post and submiting to dispatcher 
    post(1)
    
    print "calling the aggregate function",time.asctime()
    async5=Pyro4.async(dispatcher)
    async5_result= async5.aggregate()
    #temp=async5_result.value
    #print "-------------------------------------",temp
    
    os.system("rm -rf /home/ubuntu/casebook/media/photos/*")
    
    
    print "inserting USER_POST and usr_frnd in cassandra",time.asctime()
    user_frnd(1)            
    CASS.save_WALL(USER_POST)
    print "inserting DONE in USER_POST and usr_frnd in cassandra",time.asctime()
    
    
    photo_merge_done=0
    post_index_done=0
    while(1):
        if photo_merge_done==0:            
            if photo_result1.ready and photo_result2.ready and photo_result3.ready:
                photo_merge_done=1
                #merged={}
                result1 =  photo_result1.value
                result2 =  photo_result2.value
                result3 =  photo_result3.value
                print "photo Results received... Merging them", time.asctime()
                m1 = combine(result1, result2)
                merged = combine(result3, m1)
                photo_index = {}
                for keys in merged:
                    photo_index[keys] = {}
                    photo_index[keys]['photoid']=','.join(merged[keys])
                CASS.save_photo_index(photo_index)    
                print"inserted photo  in cass"
                
        if post_index_done==0:                                    
            if async5_result.ready:
                post_index_done=1  
                #user_frnd(1)
                
                #print "inserting USER_POST in cassandra",time.asctime()
                #CASS.save_WALL(USER_POST)
                """
                print"inserting WALLPOST into cassandra ",time.asctime()
                length=len(WALLPOST.keys())
                PPP=0
                temp={}
                for keys in WALLPOST:
                    PPP=PPP+1
                    temp[keys]=WALLPOST[keys]
                    if PPP==5000:
                        CASS.save_post(temp)
                        temp.clear()
                        PPP=0
                CASS.save_post(temp)
                print "completed WALLPOST in cassandra",time.asctime()
                """
        """    
        print "start copiing photos", time.asctime()
        os.system("scp -i /home/ubuntu/abhi.pem -q -r ubuntu@10.0.2.7:./distributed/photos /home/ubuntu/casebook/media/") 
        os.system("scp -i /home/ubuntu/abhi.pem -q -r ubuntu@10.0.2.8:./distributed/photos /home/ubuntu/casebook/media/") 
        os.system("scp -i /home/ubuntu/abhi.pem -q -r ubuntu@10.0.2.4:./distributed/photos /home/ubuntu/casebook/media/") 
        print "completed copiing photos", time.asctime()
        dir_name = "/home/ubuntu/casebook/media/photos/"
        photo_data_dict={}
        num_inserted = 0
        for file_name in os.listdir(dir_name):
                dirfile = os.path.join(dir_name, file_name)    
            f = open(dirfile, 'r')
            data = f.read()
            num_inserted = num_inserted + 1
            photo_data_dict[str(file_name)]={}
            photo_data_dict[str(file_name)]['data'] = data
            if num_inserted == 10:
            CASS.save_photo(photo_data_dict)
            photo_data_dict.clear()
            num_inserted = 0
        CASS.save_photo(photo_data_dict)
        print "Inserted photo's in cassandra", time.asctime()
        """
         
        if photo_merge_done==1 and post_index_done==1:
            break

        
            
        
    #post(1)
    print "DONE_____________________",time.asctime()
    return
      
      
      


            
      
      
               
if __name__ == "__main__":
    main()
