#!/usr/bin/python

from jnpr.junos import Device
from pprint import pprint as pp
from bottle import get, post, request, run, template, redirect # or route
from itertools import *
import operator
sort_by_kbytes = []
sort_by_session = []

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
    appgroups, sessions, kbytes = read_device(hostname,username,passwd)
    group_result = []
    global sort_by_session
    global sort_by_kbytes
    # for i in range(len(kbytes)):
    #     if len(appgroups[i].split(':')) > 2:     
    #          group_result.append(zip(appgroups[i].split(':').pop(), sessions[i], kbytes[i]))
    for i in izip(appgroups, sessions, kbytes):
        # if len(i[0].split(':')) > 2:
             group_result.append(i)
    sort_by_session = sorted(group_result,key=operator.itemgetter(1), reverse=True)
    sort_by_kbytes = sorted(group_result, key=operator.itemgetter(2), reverse=True)
    #print group_result
    #print sort_by_kbytes
    return template('testout',rows=sort_by_kbytes)

@get('/ag_report_sessions')
def present_ag_sessions():
    return template('testout',rows=sort_by_session)    

@get('/ag_report_kbytes')
def present_ag_sessions():
    return template('testout',rows=sort_by_kbytes) 

    ## Debug ##
    # print "App Groups: ", appgroups
    # print "App Sessions: ", sessions
    # print "Sum: ", kbytes
    # print "Done !!"

def read_device(hostname, username, passwd):         
    dev = Device(hostname,user=username,password=passwd)
    dev.open()
    print "Login successful ..."
    print (dev.facts)
    
    ### Read application group data from SRX
    apps_groups = dev.rpc.get_appid_application_group_statistics()
    appgroup_list = apps_groups.findall('appid-application-group-statistics/application-name')
    sessions_list = apps_groups.findall('appid-application-group-statistics/sessions')
    kbyte_list = apps_groups.findall('appid-application-group-statistics/bytes')

    app_groups = []    
    app_sessions = []
    k_bytes = []

    for x,y,z in zip(appgroup_list,sessions_list,kbyte_list) :
         app_groups.append(x.text[6:])
         app_sessions.append(int(y.text))
         k_bytes.append(int(z.text)) 

    dev.close()
    print "Closing device ... "
    return app_groups,app_sessions,k_bytes

run(host='localhost', port=8082)         # Start the webserver running and wait for requests
