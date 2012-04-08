import Pyro4
import time

print "Starting photo processing:", time.asctime()

photo_client=Pyro4.Proxy("PYRONAME:photo.async")
photo_async=Pyro4.async(photo_client)
photo_result1=photo_async.process_photo("http://enl.usc.edu/~cs694/casebook/config70.txt")


photo_client2=Pyro4.Proxy("PYRONAME:photo.async2")
photo_async2=Pyro4.async(photo_client2)
photo_result2=photo_async2.process_photo("http://enl.usc.edu/~cs694/casebook/config70.txt")
merged={}
while(1):
    if photo_result1.ready and photo_result2.ready:
	result1 =  photo_result1.value
	result2 =  photo_result2.value
	print "Results received... Merging them"
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
	break

print "merged results:", time.asctime()
for key in merged.keys():
	print key + '------>'+ str(merged[key])
