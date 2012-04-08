from __future__ import print_function
import time
import urllib
import Pyro4
import sys, os
from opencv.cv import *
from opencv.highgui import *


class Photo(object):
    #def __init__(self):        
        #self.photo_index={}
        #self.photo_urls={}
        #self.photo_face={}    
        
    #integration method for downloading and processing half of the photos
    def process_photo(self, confurl):
        #os.system("kill -9 `ps -eaf | grep -i worke[r] | awk '{print $2}'`") 
	photo_index={}
        photo_urls={}
        photo_face={}

	print ("Star photo processing: " ,time.asctime())
        photo_urls = self.parse(confurl)
	print ("Parsed config file: ", time.asctime())
        self.downloader(photo_urls)
	print ("Downloaded photo's:" , time.asctime())
        photo_face = self.detectfaces(photo_urls)
	print ("Face detection complete:", time.asctime())
        #form index
        for ph in photo_face.keys():
	    users = photo_urls[ph]
            for user in users:
                index_key = user+':'+str(photo_face[ph])
		photoid = ph.split('/',6)[6][5:-4]
                if index_key in photo_index.keys():
                    photo_index[index_key].add(int(photoid))
                else:
		    photo_index[index_key]= set()
                    photo_index[index_key].add(int(photoid))
        #print (self.photo_index)
	print ("Photo index generated: ", time.asctime())
    	#os.system("python worker.py &") 
	os.system("scp -i abhi.pem -q -r photos ubuntu@10.0.2.3:./casebook/media/")
        return photo_index

    def parse(self, confurl):
        """
        #Download config file
        u = urlopen(name)
        FILE_write = open('file.txt', 'w')
        FILE_write.write(u.read())
        FILE_write.close()
        """
	photo_urls = {}
	#urllib.urlretrieve(confurl, "file.txt")
        #Parse config file to get photo URL's
        file = open('conf.txt', 'r',8096)                
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
        

    def downloader(self, photo_urls):
	os.system("rm -rf photos/*")
        half = len(photo_urls.keys())/2
        count = 0
        for url in photo_urls.keys():
            if count < half:
		count = count +1
		continue
	    else:
                phname = url.split('/',6)[6][5:]
                filename = 'photos/'+phname
		urllib.urlretrieve(url, filename)
                #file = open(filename, 'w')
                #file.write(urlopen(url).read())
                #file.close()

    def detectfaces(self, photo_urls):        
	photo_face = {}
        #load image from disk
        half = len(photo_urls.keys())/2
        count = 0
        for photo in photo_urls.keys():
            if count < half:
                count = count +1
		continue
	    else:
            	imagepath = os.path.join('photos/', photo.split('/',6)[6][5:])
            	image = cvLoadImage(imagepath)                    
            	"""Converts an image to grayscale and prints the locations of any faces found"""
            	grayscale = cvCreateImage(cvSize(image.width, image.height), 8, 1)
            	cvCvtColor(image, grayscale, CV_BGR2GRAY)        
            	storage = cvCreateMemStorage(0)
            	cvClearMemStorage(storage)
            	cvEqualizeHist(grayscale, grayscale)
            	cascade = cvLoadHaarClassifierCascade('/usr/share/doc/opencv-doc/examples/haarcascades/haarcascades/haarcascade_frontalface_default.xml.gz', cvSize(1,1))
            	faces = cvHaarDetectObjects(grayscale, cascade, storage, 1.2, 2,CV_HAAR_DO_CANNY_PRUNING, cvSize(70,70))
            	#number of faces detected
            	facecount=0
            	if faces:                
               	    for f in faces:
                    	facecount = facecount+1
                    	#print("[(%d,%d) -> (%d,%d)]" % (f.x, f.y, f.x+f.width, f.y+f.height))
            
            #maintain face infor for a photo
            photo_face[photo]=int(facecount)
	    #print (photo + ':' + str(facecount))
	return photo_face


ns=Pyro4.naming.locateNS()
Pyro4.config.HOST="10.0.2.7"
d=Pyro4.core.Daemon()
uri=d.register(Photo())
ns.register("photo.async2", uri)
print("Photo2 daemon object uri:",uri)
print("Photo2 daemon running.")
d.requestLoop()
#ph = Photo()
#ph.process_photo("http://enl.usc.edu/~cs694/casebook/config70.txt")
