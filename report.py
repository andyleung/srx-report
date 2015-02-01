#!/usr/bin/python

from jnpr.junos import Device
from pprint import pprint as pp
from bottle import get, post, request, run, template, redirect # or route
from itertools import *
import operator
import pymongo

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
    
    ## read data from SRX
    appgroups, sessions, kbytes, risks, categories, subcategories = read_device(hostname='172.27.62.23',username='lab',passwd='lab123')
    
    group_result = []
    global sort_by_apps
    global sort_by_session
    global sort_by_kbytes

    for i in izip(appgroups, sessions, kbytes, risks, categories, subcategories):
             group_result.append(i)
    sort_by_apps = sorted(group_result,key=operator.itemgetter(0), reverse=False)
    sort_by_session = sorted(group_result,key=operator.itemgetter(1), reverse=True)
    sort_by_kbytes = sorted(group_result, key=operator.itemgetter(2), reverse=True)

    return template('apptable',rows=sort_by_kbytes)

@get('/ag_report_apps')
def present_ag_apps():
    return template('apptable',rows=sort_by_apps) 

@get('/ag_report_sessions')
def present_ag_sessions():
    return template('apptable',rows=sort_by_session)    

@get('/ag_report_kbytes')
def present_ag_sessions():
    return template('apptable',rows=sort_by_kbytes) 

@get('/http_report')
def present_http_report():
    return template('http_table',rows=http_table) 

@get('/subcategories_report')
def present_subcategories_report():
    subcategories_table = []
    for i in subcategories_dict.items():
        mylist = []
        if i[0] and (i[1][0] is not 0):
            #print i
            sname = i[0]
            sapps = i[1][0]
            sbytes = i[1][1]
            ssessions = i[1][2]
            mylist = [sname, sapps, sbytes, ssessions]
        if mylist:
            subcategories_table.append(mylist)
    return template('subcategories_table',rows=subcategories_table) 

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

    last_reset_date = apps[0][0].text
    appgroup_list = apps.findall('appid-application-statistics/application-name')
    sessions_list = apps.findall('appid-application-statistics/sessions')
    kbyte_list = apps.findall('appid-application-statistics/bytes')

    app_groups = []    
    app_sessions = []
    bytes = []

    for x,y,z in zip(appgroup_list,sessions_list,kbyte_list) :
         app_groups.append(x.text)
         app_sessions.append(int(y.text))
         bytes.append(int(z.text)) 



    ## Connection to mongodb
    connection = pymongo.Connection("mongodb://localhost",safe=True)
    db = connection.srx
    signatures = db.signatures
    risks = []
    categories = []
    subcategories = []
    characteristic = []
    top_apps = 35
    http_apps = []
    http_apps_category = []
    http_apps_bytes = []
    http_apps_sessions = []
    http_apps_risk = []
    
    global subcategories_dict
    subcategories_dict = {u'Networking': [0, 0, 0], u'Image-Sharing': [0, 0, 0], u'Travel': [0, 0, 0], 
       u'Multimedia': [0, 0, 0], u'Advertisements': [0, 0, 0], u'Authentication': [0, 0, 0], u'P2P': [0, 0, 0], 
       u'File-Servers': [0, 0, 0], u'Monitoring': [0, 0, 0], u'VOIP': [0, 0, 0], u'SCADA': [0, 0, 0], 
       u'SCM': [0, 0, 0], u'Gaming': [0, 0, 0], u'Infrastructure': [0, 0, 0], u'Shopping': [0, 0, 0], 
       u'Finance': [0, 0, 0], u'Real-Estate': [0, 0, 0], u'File-Sharing': [0, 0, 0], u'Applications': [0, 0, 0], 
       u'RPC': [0, 0, 0], u'Portal': [0, 0, 0], u'Proxy': [0, 0, 0], u'Encryption': [0, 0, 0], u'News': [0, 0, 0], 
       u'divers': [0, 0, 0], u'Anonymizer': [0, 0, 0], u'Social-Networking': [0, 0, 0], u'Search': [0, 0, 0], 
       u'Video-Streaming': [0, 0, 0], u'nil': [0, 0, 0], u'Database': [0, 0, 0], u'Mobile': [0, 0, 0], 
       u'Instant-Messaging': [0, 0, 0], u'Mail': [0, 0, 0], u'Interactive-Desktop': [0, 0, 0], u'Command': [0, 0, 0], 
       u'Audio-Streaming': [0, 0, 0], u'Directory': [0, 0, 0], u'Messaging': [0, 0, 0], u'Tunneling': [0, 0, 0], 
       u'Backup': [0, 0, 0], u'Wiki': [0, 0, 0], u'Web-Based': [0, 0, 0], u'Business': [0, 0, 0], u'Reference': [0, 0, 0], 
       u'CDN': [0, 0, 0], u'Blogging': [0, 0, 0], u'Backdoors': [0, 0, 0], u'Legacy': [0, 0, 0], u'Protocols': [0, 0, 0], 
       u'Remote-Access': [0, 0, 0], None: [0, 0, 0], u'Forums': [0, 0, 0], u'Transport': [0, 0, 0]}

    character_dict = {'Known Vulnerabilities':0,'Can Leak Information':0,
              'Loss of Productivity':0,'Supports File Transfer':0,'Prone to Misuse':0,
              'Carrier of Malware':0,'Bandwidth Consumer':0,'Evasive':0,'Capable of Tunneling':0}

    ## Find the risk, category, and subcategory from mongodb
    for each_app in app_groups:
      total_sessions = app_sessions[app_groups.index(each_app)]
      total_bytes = bytes[app_groups.index(each_app)]
      cursor = signatures.find({"type": normalize(each_app)}) 
      app_risk = 0
      characteristic = []
      for result in cursor:
             app_risk = result['risk']
             category = result['category']
             subcategory = result['subcategory']
             #print "App: ", each_app ," Risk: ", app_risk, "category: ", category, "subcategory: ", subcategory
             characteristic = result['characteristic']
      ## Application that use HTTP 
             if result['ports'] is not None:
                  if ('HTTP' or 'HTTPS') in result['ports']:
                        http_apps.append(normalize(each_app))
                        http_apps_category.append(result['subcategory'])
                        http_apps_bytes.append(total_sessions) 
                        http_apps_sessions.append(total_bytes)
                        http_apps_risk.append(result['risk'])
      risks.append(str(app_risk))
      categories.append(category)
      subcategories.append(subcategory)

      #Update Application Subcategories, increment: App counts, bytes, sessions
      if subcategory:
          subcategories_dict[subcategory][0] = subcategories_dict[subcategory][0] +1
          subcategories_dict[subcategory][1] += int(total_bytes)
          subcategories_dict[subcategory][2] += int(total_sessions)
    
    #build the http_table
    global http_table
    for i in izip(http_apps, http_apps_category, http_apps_risk, http_apps_bytes, http_apps_sessions):
             http_table.append(i)

    return app_groups,app_sessions, bytes, risks, categories, subcategories

run(host='localhost', port=8082)         # Start the webserver running and wait for requests
