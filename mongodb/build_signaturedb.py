#!/usr/bin/python

import pymongo
import sys
import json
import xml.etree.ElementTree as ET
from lxml import etree
from jnpr.junos import Device


def get_db():
    try:
        connection = pymongo.Connection("mongodb://localhost",safe=True)
        db = connection.srx
        return db
    except pymongo.errors.ConnectionFailure, e:
        print "Could not connect to MongoDB: %s" % e 
    

def insertdb(db,host,user,password):
   dev = Device(host='172.27.62.23',user='lab',password='lab123') 
   dev.open()
   print "Opening Device ... "
   ##dev.timeout = 300
   root = dev.rpc.get_appid_application_signature_detail(dev_timeout=300)
   flash("Finish getting signatures")
   dev.close()

   count = 0
   for sig in root.findall('.//application-signature-detail'):
         data={'characteristic':[],'ports':[],'alias':[]}
         data['name'] = sig.find('application-signature-detail-header/application-name').text
         data['type']= data['name'][6:]
         data['description'] = sig.find('application-signature-detail-header/application-description').text
         data['app-id'] = int(sig.find('application-signature-detail-header/application-id').text)

         data['risk'] = ""
         data['category'] = ""
         data['subcategory'] = "" 
         for tags in sig.findall('application-signature-detail-header/application-tag-list/application-tag'):
             
             tag = tags.find('application-tag-name').text
             value = tags.find('application-tag-value').text
             #print "tag: ", tag, "value: ", value
             if tag == 'risk':
                data['risk'] = int(value)
             elif tag == 'subcategory':
                data['subcategory'] = value
             elif tag == 'category':
                data['category'] = value
             elif tag == 'characteristic':
             	data['characteristic'].append(value)
         
         ## List of the ports is different from above. So treat it special.
         ports = sig.find('application-signature-detail-header/application-over-list')
         if ports is not None:
             for port in ports.iter('application-app-name'):
                #print "Ports: ", port.text
                data['ports'].append(port.text)

         aliases = sig.find('application-signature-detail-header/application-alias-list')
         if aliases is not None:
              for alias in aliases.iter('application-alias-name'):
                 #print "Alias: ", alias.text
                 data['alias'].append(alias.text)

         #Finally, insert into the mongodb
         db.signatures.insert(data)
   print "Insert to MongoDB ... done"

         #Or, query in this way also works:
        #data['application-type']= sig[0][1].text
         #data['description']= sig[0][2].text
         #data['app-id'] = sig[0][3].text
                     
if __name__ == "__main__":
    db = get_db()
    db.signatures.drop()
    insertdb(db)
    num = db.signatures.find().count()
    print "Total signatures: ", num
    

