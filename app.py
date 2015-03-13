#!/usr/bin/python

from flask import Flask, render_template, request, flash, jsonify, url_for
from jnpr.junos import Device
from pprint import pprint as pp
from math import log 
from subprocess import call 
import os
import time
import json
import pdfkit
import pymongo
import reportDAO

app = Flask(__name__)

app.secret_key = "juniper"
connection_string = "mongodb://localhost"
connection = pymongo.MongoClient(connection_string)
database = connection.srx
collection_name = 'report'

report = reportDAO.ReportDAO(database)

def read_device(hostname, username, passwd, code):         
    dev = Device(hostname,user=username,password=passwd)
    dev.open()
    print "Login successful ..."
    ##print (dev.facts)
    
    ### Read application group data from SRX
    ### lab@srx2> show services application-identification statistics applications 
    if code == 'status': 
         print "Getting status ..."   
         apps = dev.rpc.get_appid_application_statistics()
         apps_groups = dev.rpc.get_appid_application_group_statistics()
    elif code == 'signatures':
         print "Getting signatures ..."
         root = dev.rpc.get_appid_application_signature_detail(dev_timeout=600)
         print "Finish getting signatures ..."
         dev.close()
         return root     
    else:
         print "Device Error"
    print "Closing device ... "
    dev.close()

    if database.report:
         print "Data already exist. Clearing old data."
         database.report.drop()

    if report.insert_entry(apps):
         print "Insert Successful!!"

# displays the initial form
@app.route('/', methods=['GET','POST'])
##@app.route('/report',methods=['GET','POST'])
def present_get_input():
    browser = ''
    browser = request.user_agent.browser
    print "Browser: ",browser
    if (browser == 'firefox'):
        flash("Please use Chrome / IE / Safari for better displays")
    if request.method == 'POST':
        hostname = request.form['hostname']
        username = request.form['user']
        passwd = request.form['password']

        read_device(hostname,username,passwd,code='status')

        cursor = report.sort_by_kbytes()
        sort_by_kbytes = []
        for i in cursor:
          #print i
          sort_by_kbytes.append(i)
        return render_template('apptable.html',rows=sort_by_kbytes)
    return render_template("index.html")

@app.route("/build",methods=['GET','POST'])
def build():
  if request.method == 'POST':
      hostname = request.form['hostname']
      username = request.form['user']
      password = request.form['password']
      root = read_device(hostname,username,password,code='signatures')
      count = 0
      database.signatures.drop()
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
             database.signatures.insert(data)
      print "Insert to MongoDB ... done"
      flash ("Building signatures database ... done")
      return render_template('build.html')
  return render_template('build.html')

@app.route('/report_sessions')
def present_sessions():
    cursor = report.sort_by_sessions()
    sort_by_sessions = []
    for i in cursor:
      #print i
      sort_by_sessions.append(i)
    return render_template('apptable.html',rows=sort_by_sessions)  

@app.route('/report_apps')
def present_apps():
    cursor = report.sort_by_apps()
    sort_by_apps = []
    for i in cursor:
      #print i
      sort_by_apps.append(i)
    return render_template('apptable.html',rows=sort_by_apps)  

@app.route('/report_kbytes')
def present_kbytes():
    cursor = report.sort_by_kbytes()
    sort_by_kbytes = []
    for i in cursor:
      #print i
      sort_by_kbytes.append(i)    
    return render_template('apptable.html',rows=sort_by_kbytes) 


@app.route('/report_risk')
def present_risks():
    cursor = report.sort_by_risk()
    sort_by_risk = []
    for i in cursor:
      #print i
      sort_by_risk.append(i)    
    return render_template('apptable.html',rows=sort_by_risk)

@app.route('/char_bar')
def char_bar():
    cursor = report.sort_by_characteristic()
    #print "Cursor: " , cursor
    sort_by_characteristic = []
    for i in cursor['result']:
         sort_by_characteristic.append(i)
    #print 'json: ',jsonify(sort_by_characteristic)
    return render_template('char_bar.html')

@app.route('/char_pie')
def char_pie():
    return render_template('char_pie.html')

@app.route('/char_data')
def char_data():
    cursor = report.sort_by_characteristic()
    sort_by_characteristic = []
    for i in cursor['result']:
         sort_by_characteristic.append(i)
    #print sort_by_characteristic
    return json.dumps(sort_by_characteristic)

@app.route('/app_bar',methods=['POST','GET'])
@app.route('/app_bar/<int:num>')
def app_bar(num=15):
    if request.method == 'POST':
           num = int(request.form['num'])
           print "POST: Number of Apps: ", num
           return render_template('app_bar.html',app_num=num)
    else:
       print "GET: Number of Apps "
       return render_template('app_bar.html',app_num=num)


@app.route('/app_pie')
def app_pie():
    return render_template('app_pie.html')

@app.route('/app_data/<int:limit>')
def app_data(limit):
    cursor = report.group_apps(limit)
    sort_by_apps = []
    for i in cursor['result']:
         sort_by_apps.append(i)
    return json.dumps(sort_by_apps)

@app.route("/data")
def data():
    RESULTS = {'children': []}
    cursor = report.bubble_apps()
    for i in cursor['result']:
        ##print i
        ##print "count: ",i['count'],"id: ",i['_id'],"groups: ",i['category']
        RESULTS['children'].append({
                'name': i['_id'],
                'value': log(i['count']),
                'group': i['main_group'][0]
        })
    #print RESULTS
    return jsonify(RESULTS)


@app.route("/app_bubble")
def app_bubble():
    return render_template("app_bubble.html")

@app.route("/category_bar")
def category_bar():
    return render_template("category_bar.html")

@app.route("/category_pie")
def category_pie():
    return render_template("category_pie.html")

@app.route('/category_data')
def category_data():
    cursor = report.sort_by_category()
    sort_by_category = []
    for i in cursor['result']:
         sort_by_category.append(i)
    ##print sort_by_category
    return json.dumps(sort_by_category)

@app.route("/subcategory_bar")
def subcategory_bar():
    return render_template("subcategory_bar.html")

@app.route('/subcategory_pie')
def subcategory_pie():
    return render_template('subcategory_pie.html')

@app.route('/subcategory_data')
def subcategory_data():
    cursor = report.sort_by_subcategory()
    sort_by_subcategory = []
    for i in cursor['result']:
         sort_by_subcategory.append(i)
    ##print sort_by_subcategory
    return json.dumps(sort_by_subcategory)

@app.route('/http_apps')
def http_apps():
    cursor = report.http_apps()
    rows = []
    for i in cursor:
        ## print "This app: ",i
        rows.append({
            "name" : i['name'],
            "sessions": i['sessions'],
            "bytes": i['bytes'],
            "category": i['category'],
            "is_encrypted": i['is_encrypted']
            })
    return render_template('http_apps.html',rows=rows)

@app.route('/app_groups_data')
def app_groups_data():
    mydata2 = {
    "name": "Root", 
    "children": [
        {
            "name": "junos", 
            "children": [
                {
                    "name": "infrastructure", 
                    "children": [
                        {
                            "name": "directory"
                        }, 
                        {
                            "name": "networking"
                        }, 
                        {
                            "name": "encryption"
                        }
                    ]
                }, 
                {
                    "name": "p2p", 
                    "children": [
                        {
                            "name": "file-sharing"
                        }
                    ]
                }, 
                {
                    "name": "remote-access", 
                    "children": [
                        {
                            "name": "command"
                        }
                    ]
                }, 
                {
                    "name": "web", 
                    "children": [
                        {
                            "name": "social-networking", 
                            "children": [
                                {
                                    "name": "facebook"
                                }, 
                                {
                                    "name": "linkedin"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ]}

    return json.dumps(mydata2)

@app.route('/app_groups')
def app_groups():
        return render_template('app_groups.html')

@app.route('/block_apps', methods=['POST'])
def block_apps():
        block_list = list(set(request.form.getlist('block-apps'))) 
        policyhead = '''set security policies from-zone trust to-zone untrust policy policy1 match source-address any
set security policies from-zone trust to-zone untrust policy policy1 match destination-address any
set security policies from-zone trust to-zone untrust policy policy1 match application any
set security policies from-zone untrust to-zone trust policy policy1 then permit application-services application-firewall rule-set rs1
set security application-firewall rule-sets rs1 rule r1 match dynamic-application [ 
'''

        policytail = ''' ] 
set security application-firewall rule-sets rs1 rule r1 then deny
set security application-firewall rule-sets rs1 default-rule deny 
'''
        return render_template('block_apps.html',block_list=block_list,policyhead=policyhead,policytail=policytail) 

@app.route('/report')
def report_pdf():
    # Make a PDF from another view
    return render_template('report.html')

@app.route('/build_reports', methods=['POST'])
def build_reports():
    reports = []
    reports = request.form.getlist('reports') 
    print "Get: ", reports
    if reports:
       # for i in reports:
       #     LINK = "http://127.0.0.1:5000/"
       #     call(["/usr/local/bin/wkhtmltopdf",LINK+i,"report/"+i+".pdf"])
       flash ("Reports are stored at '/report' directory...")
       return render_template('build_report.html',reports=reports)
    return render_template('build_report.html',reports=reports)

if __name__ == '__main__':
	app.run(
           host='0.0.0.0',
           port=5000,
           debug=True)

