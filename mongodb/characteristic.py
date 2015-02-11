#!/usr/bin/python

import pymongo
import sys
from pprint import pprint as pp

def main():
	connection = pymongo.Connection('mongodb://localhost', safe = True)
	db = connection.srx
	foo = db.report
	doc = foo.aggregate([{'$unwind':'$characteristic'},{'$group':{"_id":"$characteristic","count":{"$sum":1}}},{'$project':{"_id":1,"count":1}}])
        print "Doc: ",doc
        for i in doc['result']:
             print "Result: ",i

if __name__ == '__main__':
    main()



