import random

USERS=10
frnd_per_usr=8
users= ((USERS/frnd_per_usr)+1 ) * frnd_per_usr -1
photo_per_usr=1
post_per_usr=2

f = open('conf.txt', 'w')

# generating users
for n in range(1,users+1):
    value = "user u"+str(n) +" \"user"+str(n)+ "\" \"foo\"\n"
    s = str(value)
    f.write(s)
    
# generating friend relationships
iterations=users/frnd_per_usr
#####print 'iterations are', iterations
current_usr=1
count=0
for x in range(1,iterations+1):
    #####print 'in x'
    #frnd=[]
    #del frnd[0:len(frnd)]
    #current_usr= x * 
    count1 =0
    
    #####print 'current usr  in x ',current_usr
    for y in range(current_usr,current_usr+frnd_per_usr):
        #####print 'now for user',y
        for z in range(1,frnd_per_usr-count1+1): 
            ####print 'friend is',current_usr +z
            # ####print 'z is',z
            value= "friend u"+str(current_usr)+" u"+str(current_usr+z)+"\n"
            s = str(value)
            f.write(s)
        ####print 'in y'
        current_usr= current_usr + 1
        count1=count1+1
    count=count+1
    current_usr=frnd_per_usr*x + 2
    #####print 'in x 2'        
        
# generating wallposts for each user        
for x in range(1,users+1):
    for y in range(1,post_per_usr+1):
        value= "wallpost u"+str(x)+" \"this is my wall post no:"+str(y)+" of user "+ str(x) +"\"\n"
        s = str(value)
        f.write(s)         
        
# generating photos for each user        
for x in range(1,users+1):
    for y in range(1,photo_per_usr+1):
        value= "photo u"+str(x)+" http://enl.usc.edu/~cs694/photos/photo"+str(random.randint(1,10))+".jpg\n"
        s = str(value)
        
        f.write(s) 
