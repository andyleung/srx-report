#!/usr/bin/python

from jnpr.junos import Device
from pprint import pprint as pp
from bottle import get, post, request, run, template, redirect # or route
from itertools import *
import operator
import pymongo
import reportDAO

sort_by_apps = []
sort_by_kbytes = []
sort_by_session = []
http_table = []
subcategories_dict = {}
sort_by_characteristics = []

# displays the initial form
@get('/report')
def present_get_input():
    return template("get_input",
                           dict(username="", password="",
                                hostname="",
                                verify_error =""))

@post('/report')
def present_show_input():
    appgroups = []
    sessions = []
    kbytes = []

    hostname = request.forms.get('hostname')
    username = request.forms.get('username')
    passwd = request.forms.get('password')
    
    read_device(hostname='172.27.62.23',username='lab',passwd='lab123')

    cursor = report.sort_by_kbytes()
    sort_by_kbytes = []
    for i in cursor:
      print i
      sort_by_kbytes.append(i)

    return template('apptable2',rows=sort_by_kbytes)

@get('/ag_report_apps')
def present_ag_apps():
    cursor = report.sort_by_apps()
    sort_by_apps = []
    for i in cursor:
      print i
      sort_by_apps.append(i)
    return template('apptable2',rows=sort_by_apps) 

@get('/ag_report_sessions')
def present_ag_sessions():
    cursor = report.sort_by_sessions()
    sort_by_sessions = []
    for i in cursor:
      print i
      sort_by_sessions.append(i)
    return template('apptable2',rows=sort_by_sessions)    

@get('/ag_report_kbytes')
def present_ag_sessions():
    cursor = report.sort_by_kbytes()
    sort_by_kbytes = []
    for i in cursor:
      print i
      sort_by_kbytes.append(i)    
    return template('apptable2',rows=sort_by_kbytes) 

@get('/ag_report_risk')
def present_ag_sessions():
    cursor = report.sort_by_risk()
    sort_by_risk = []
    for i in cursor:
      print i
      sort_by_risk.append(i)    
    return template('apptable2',rows=sort_by_risk)

@get('/ag_report_characteristic')
def present_characteristic_report():
    cursor = report.sort_by_characteristic()
    sort_by_characteristic = []
    for i in cursor['result']:
        print i
        sort_by_characteristic.append(i)
    return template('chartable',rows=sort_by_characteristic)     

@get('/http_report')
def present_http_report():
    return template('http_table',rows=http_table) 

@get('/subcategory_report')
def present_subcategory_report():
    cursor = report.sort_by_subcategory()
    sort_by_subcategory = []
    for i in cursor['result']:
        print i
        if i['_id']:
            sort_by_subcategory.append(i)    
    return template('subcategory_table',rows=sort_by_subcategory) 

"""Normalize SRX app names
"""
def normalize(str):
   if len(str.split('_')) == 2:
       return '-'.join(str.split('_'))
   else:
       return str

def read_device(hostname, username, passwd):         
    dev = Device(hostname,user=username,password=passwd)
    dev.open()
    print "Login successful ..."
    ##print (dev.facts)
    
    ### Read application group data from SRX
    ### lab@srx2> show services application-identification statistics applications     
    apps = dev.rpc.get_appid_application_statistics()
    dev.close()
    print "Closing device ... "

    if report.insert_entry(apps):
         print "Insert Successful!!"

connection_string = "mongodb://localhost"
connection = pymongo.MongoClient(connection_string)
database = connection.srx
collection_name = 'report'

report = reportDAO.ReportDAO(database)

run(host='localhost', port=8082)         # Start the webserver running and wait for requests
