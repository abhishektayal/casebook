import os
import Pyro4
import urllib
import time

class downloader_class(object):
    def __init__(self):
        new_obj=0
        
    def download(self,filename):
        
        print "inside download function.... killing worker"
        os.system("kill -9 `ps -eaf | grep -i worke[r] | awk '{print $2}'`")
        print "start",time.asctime()
        #u = urllib.urlretrieve(filename,"file.txt")
        os.system("scp -i abhi.pem ubuntu@10.0.2.3:./casebook/distributed/file.txt .")
        print "downloaded file",time.asctime()     
        os.system("python worker.py &")
         


ns=Pyro4.naming.locateNS()
Pyro4.config.HOST="10.0.2.6"
daemon=Pyro4.core.Daemon()
Download=downloader_class()
#Download.download('http://enl.usc.edu/~cs694/casebook/config70.txt')
uri=daemon.register(Download)
ns.register("download_daemon", uri)
print "downloader ready"
daemon.requestLoop()    