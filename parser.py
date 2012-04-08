import cass
import re
import time

def user(val):
    stat ={}
    #print 'in user(), val is ',val
    match= val.split(' ',2)
    password= match[2].split('\n',1)
    
    stat['actual_name']=match[1][1:-1]
    stat['password']=password[0][1:-1]
    #print 'actual name is:',match[0]
    cass.save_user(match[0],stat)
    

def wallpost(val):
    stat ={}
#   print 'in wallpost(), val is ',val
    match= val.split(' ',1)
#   print 'post is',match[0]
    post= match[1].split('\n',1)
    stat['body']=post[0][1:-1]
    
    #print 'body is:',stat['body']
    cass.save_post(match[0],stat)

def photo(val):
    #print 'in photo()'
    match= val.split(' ',1)
    photo_url= match[1].split('\n',1)
    #print 'url is:',photo_url
    cass.save_photo(match[0], photo_url[0])

def friend(val):   
    #print 'in friend()'
    match= val.split(' ',1)
    cass.add_friend(match[0],match[1][0:-1])     
                        
options = { 
                'user':user,
                'wallpost':wallpost,
                'photo':photo,
                'friend':friend
           }


def parse():
    print time.asctime()
    f = open('conf.txt', 'r')
    
    for line in f:
     
        match = line.split(' ', 1) 
        if match:
            if match[0]  in options.keys():
                #print 'found the key ',match.group(1)
                options[match[0]](match[1]) 
            else:
                #print 'found the key ' ':friend'
                friend(line)
                  
                   
    print time.asctime()
    
def main():
    parse()      
               
if __name__ == "__main__":
    main()
