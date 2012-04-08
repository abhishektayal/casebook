import sys
import pycassa
from pycassa.system_manager import *
import os
con = SystemManager('10.0.2.3:9160')

def create_schema():
	print "inside create_schema.."
	con.create_keyspace('Casebook_test', strategy_options={"replication_factor":"1"})
	print"111111111"
	con.create_column_family('Casebook_test', 'User')
	print"22222222"
	con.create_column_family('Casebook_test', 'Friends')
	con.create_column_family('Casebook_test', 'Photo_Album')
	con.create_column_family('Casebook_test', 'Wall')
	con.create_column_family('Casebook_test', 'Post')
	con.create_column_family('Casebook_test', 'Photo_store')
	con.create_column_family('Casebook_test', 'Photo')

def drop_schema():
	#con. drop_column_family('Post')
	print "in drop"
        try:
            con.drop_keyspace('Casebook_test')
            create_schema()
            print "there....."
            return 0
        except:            
            return 1

#def kill_java():
#	pid = os.system("ps -ef | grep java | grep -v grep | awk '{print $2}'")
#	os.kill(pid, signal.SIGKILL)
#	os.system("kill "+ pid)
	
def main(argv):
	#for arg in sys.argv:
		#print arg
		

	if argv == 'create':
		print "got create schema input"
		create_schema()
	if argv == 'drop':
		print "got drop schema input"
		drop_schema()
		
if __name__== '__main__':
	main(sys.argv[1])
