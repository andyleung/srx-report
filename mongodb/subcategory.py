#!/usr/bin/python

import pymongo
import sys
from pprint import pprint as pp

def main():
	connection = pymongo.Connection('mongodb://localhost', safe = True)
	db = connection.srx
	foo = db.report
	doc = foo.aggregate([{'$group':{"_id":"$subcategory","App count":{"$sum":1},"Sessions":{"$sum":"$sessions"},"Bytes":{"$sum":"$bytes"}}}])
        print "Doc: ",doc
        for i in doc['result']:
             print "Result: ",i

if __name__ == '__main__':
    main()



