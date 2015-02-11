#!/usr/bin/python

import sys
import re
import os
import shutil
import commands
import pymongo
import json

from itertools import *
from jnpr.junos import Device
from pprint import pprint as pp

"""Display SRX AppTrack Table
"""
def normalize(str):
   if len(str.split('_')) == 2:
       return '-'.join(str.split('_'))
   else:
       return str

def print_app_table(dev):

## Connection to mongodb
    connection = pymongo.Connection("mongodb://localhost",safe=True)
    db = connection.srx
    signatures = db.signatures

    """ Print the application tracking table. """
    applications = []
    bytes = []
    sessions = []
    encrypted = []
    risks = []
    categories = []
    subcategories = []
    http_apps = []
    http_apps_category = []
    http_apps_bytes = []
    http_apps_sessions = []
    http_apps_risk = []
    top_apps = 35
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
    output_file = open('app_overview.html','w')
    top_apps_file = open('top35.html','w')
    subcategories_file = open('subcategories.html','w')
    http_apps_file = open('http_apps.html','w')

    ## Retrieve data from SRX
    dev.open()
    jj = dev.cli("show services application-identification statistics applications")
    kk = jj.splitlines()
    tsize = len(kk)

    """ Writing the data into table """
    for i in range(3,tsize):
      information = kk[i].split()
      applications.append(normalize(information[0]))
      sessions.append(information[1])
      bytes.append(int(information[2]))
      encrypted.append(information[3])
## Debug ##
##    print "Application :", applications
##    print "Sessions :", sessions
##    print "Bytes :", bytes
##    print "Encrypted :", encrypted

## Find the risk, category, and subcategory from mongodb
      cursor = signatures.find({"type": normalize(information[0])}) 
      app_risk = 0
      characteristic = []
      for result in cursor:
             app_risk = result['risk']
             category = result['category']
             subcategory = result['subcategory']
      #print "App: ", information[0]," Risk: ", app_risk, "category: ", category, "subcategory: ", subcategory
             characteristic = result['characteristic']
      ## Applicatoin that use HTTP 
             if result['ports'] is not None:
                  ## print information[0]," : ", result['ports']
                  if 'HTTP' in result['ports'] or 'HTTPS' in result['ports']:
                        http_apps.append(normalize(information[0]))
                        http_apps_category.append(result['subcategory'])
                        http_apps_bytes.append(information[2])
                        http_apps_sessions.append(information[1])
                        http_apps_risk.append(result['risk'])

      #print "App: ", information[0], "has these characteristics: ", characteristic
      risks.append(str(app_risk))
      categories.append(category)
      subcategories.append(subcategory)
      for i in characteristic:
           character_dict[i] = character_dict[i]+1

      #Update Application Subcategories, increment: App counts, bytes, sessions
      subcategories_dict[subcategory][0] = subcategories_dict[subcategory][0] +1
      subcategories_dict[subcategory][1] += int(information[2])
      subcategories_dict[subcategory][2] += int(information[1])


    ## Write to app_overview1.html
    output_file.write('<!DOCTYPE html><html lang="e"><head><meta charset="UTF-8"><title>SRX App Report</title><link rel="stylesheet" href="style.css"></head>')
    output_file.write("<html><h2>Applications Analysis  Overview</h2><body>\n")
    output_file.write("<table>\n")
    output_file.write("<tr><th>"+"Applications"+"</th><th>"+"Risk"+"</th><th>"+
            "Category"+"</th><th>"+"Sub-Category"+"</th><th>"+"Sessions"+"</th><th>"
            +"Bytes"+"</th><th>"+"Encrypted"+"</th></tr>") 
    
    for i in range(0, tsize-3):
        if int(risks[i]) == 5:
            output_file.write("<tr class='warm5'><th class='hot5'>"+applications[i]+"</th><td>"+str(risks[i])+"</td><td>"+categories[i]+"</td><td>"+subcategories[i]+"</td><td>"+sessions[i]+"</td><td>"+str(bytes[i])+"</td><td>"+encrypted[i]+"</td></tr>")
        elif int(risks[i])  == 4:
            output_file.write("<tr class='warm4'><th class='hot4'>"+applications[i]+"</th><td>"+str(risks[i])+"</td><td>"+categories[i]+"</td><td>"+subcategories[i]+"</td><td>"+sessions[i]+"</td><td>"+str(bytes[i])+"</td><td>"+encrypted[i]+"</td></tr>")
        else:
            output_file.write("<tr><th>"+applications[i]+"</th><td>"+str(risks[i])+"</td><td>"+categories[i]+"</td><td>"+subcategories[i]+"</td><td>"+sessions[i]+"</td><td>"+str(bytes[i])+"</td><td>"+encrypted[i]+"</td></tr>")
    output_file.write("</table></body></html>")
    output_file.close()
    
    ## Output Application Behavorial Characteristics
    print "Application behavorial characteristics: ", character_dict

    ## Top 35 Apps sorted by bytes ##
    sorted_lists = sorted(izip(applications,risks,categories,subcategories,bytes), reverse=True, key=lambda x:x[4])
    applications, risks, categories, subcategories, bytes = [[x[i] for x in sorted_lists] for i in range(5)]


    #Write to top35.html
    top_apps_file.write("<html><h2>Top 35 Applications</h2><body>\n")
    top_apps_file.write("<table border=1 frame=box rules=all>\n")
    top_apps_file.write("<tr><td>"+"Top 35 Apps"+"</td><td>"+"Risk"+"</td><td>"+"Category"+"</td><td>"+"Sub-Category"+"</td><td>"+"Bytes"+"</td></tr>") 
    print_length = len(bytes)
    if print_length > top_apps:
         print_length = top_apps
    for i in range(print_length):
        top_apps_file.write("<tr><td>"+applications[i]+"</td><td>"+risks[i]+"</td><td>"+categories[i]+"</td><td>"+subcategories[i]+"</td><td>"+str(bytes[i])+"</td></tr>") 
    top_apps_file.write("</table></body></html>")
    top_apps_file.close()

    ## print "Size: ", len(bytes), "The byte order: ",bytes

    ## Write to subcategories.hml, Top Application Subcategories
    subcategories_file.write("<html><h2>Top Application Subcategories</h2><body>\n")
    subcategories_file.write("<table border=1 frame=box rules=all>\n")
    subcategories_file.write("<tr><td>"+"Sub-Category"+"</td><td>"+"Num of Applications"+"</td><td>"+"Bytes"+"</td><td>"+"Sessions"+"</td><tr>")     
    ##print "subcategories_dict: ", subcategories_dict
    for i in subcategories_dict.items():
        if i[1][0] is not 0:
            sname = i[0]
            sapps = i[1][0]
            sbytes = i[1][1]
            ssessions = i[1][2]
            subcategories_file.write("<tr><td>"+sname+"</td><td>"+str(sapps)+"</td><td>"+str(sbytes)+"</td><td>"+str(ssessions)+"</td><tr>")     
    subcategories_file.write("</table></body></html>")

    ## Applicatoin that use HTTP or HTTPS
    ##print "Apps that use HTTP or HTTPS: " , http_apps, "risks: ", http_apps_risk, "Sessions: ", http_apps_sessions, "Bytes: ", http_apps_bytes, "Sub-category: ", http_apps_category 
    http_apps_file.write("<html><h2>Applications That Use HTTP or HTTPS</h2><body>\n")
    http_apps_file.write("<table border=1 frame=box rules=all>\n")
    http_apps_file.write("<tr><td>"+"HTTP Applications"+"</td><td>"+"Risks"+"</td><td>"+"Bytes"+"</td><td>"+"Sessions"+"</td><tr>")     
    ##print "subcategories_dict: ", subcategories_dict
    for i in range(len(http_apps)):
        http_apps_file.write("<tr><td>"+http_apps[i]+"</td><td>"+str(http_apps_risk[i])+"</td><td>"+str(http_apps_bytes[i])+"</td><td>"+str(http_apps_sessions[i])+"</td><tr>")     
    http_apps_file.write("</table></body></html>")


def print_appgroup_table(dev):
    """ Print the application tracking table. """
    appgroup = []
    app_sessions = []
    kbytes = []
    output_file = open('app_usage_by_group.html','w')
    dev.open()
    
    ### Read application group data from SRX
    apps_groups = dev.rpc.get_appid_application_group_statistics()
    sessions_list = apps_groups.findall('appid-application-group-statistics/sessions'):
    appgroup_list = apps_groups.findall('appid-application-group-statistics/application-name'):
    kbyte_list = apps_groups.findall('appid-application-group-statistics/bytes'):
    
    for x,y,z in zip(apps_groups,sessions_list,kbyte_list) :
         app_sessions.append(x.text)
         appgroup.append(y.text)
         kbytes.append(z.text)     

    #for i in apps_groups.findall('appid-application-group-statistics/sessions'):
         #print "sessions: ", i.text
         #app_sessions.append(i.text)
    #for i in apps_groups.findall('appid-application-group-statistics/application-name'):
         #appgroup.append(i.text)
         #print "app groups: ", i.text
    #for i in apps_groups.findall('appid-application-group-statistics/bytes'):
         #kbytes.append(i.text)     
         #print "kbytes: ", i.text

    ##jj = dev.cli("show services application-identification statistics application-groups")         
    ##kk = jj.splitlines()
    ##tsize = len(kk)
    ##for i in range(1,tsize):
    ##  information = kk[i].split()
    ##  appgroup.append(information[0])
    ##  app_sessions.append(information[1])
    ##  kbytes.append(information[2])

    output_file.write("<html><h2>Application Usage by Group</h2><body>\n")
    output_file.write("<table border=1 frame=box rules=all>\n")
    output_file.write("<tr><td>"+"Application Group"+"</td><td>"+"Sessions"+"</td><td>"+"Kilo Bytes "+"</td></tr>") 
    for i in range(len(kbytes)):
        if len(appgroup[i].split(':')) > 2:
             output_file.write("<tr><td>"+appgroup[i].split(':').pop()+"</td><td>"+app_sessions[i]+"</td><td>"+kbytes[i]+"</td></tr>") 
    output_file.write("</table></body></html>")
    output_file.close()


def main():
    args = sys.argv[1:]
    if not args:
       print "usage: [host] [user] [password]";
       sys.exit(1)
    host = args[0] 
    username = args[1] 
    passwd = args[2] 

    dev = Device(host,user=username,password=passwd)
    ## print_app_table(dev)
    print_appgroup_table(dev)
## end main() ##

if __name__ == "__main__":
    main()
    
