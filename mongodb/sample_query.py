#!/usr/bin/python

import pymongo
import sys
from pprint import pprint as pp

def findone(name):
	connection = pymongo.Connection('mongodb://localhost', safe = True)
	db = connection.srx
	foo = db.signatures

	#query = '{"type":'+name+'}'

	try: 
		doc = foo.find({'type':name})
		#doc = foo.find(query)
	except:
		print "Unexpected Error: ", sys.exc_info()[0]

	##print "Return: ", doc
	i = 1
        for signature in doc:
           for key in signature:
	        print "<",key,"> :", signature[key]
           ##print "======="
           ##print "The name is: ", signature['type']
def main():
    args = sys.argv[1:]
    if not args:
       print "usage: [app_name] ";
       sys.exit(1)
    else:
       findone(args[0])    
## end main() ##

if __name__ == '__main__':
    main()



