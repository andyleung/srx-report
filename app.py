#!/usr/bin/python

from flask import Flask, render_template, request, flash, jsonify
from jnpr.junos import Device
from pprint import pprint as pp
from math import log 
import json
import pymongo
import reportDAO

app = Flask(__name__)

app.secret_key = "juniper"
connection_string = "mongodb://localhost"
connection = pymongo.MongoClient(connection_string)
database = connection.srx
collection_name = 'report'

report = reportDAO.ReportDAO(database)

def read_device(hostname, username, passwd):         
    dev = Device(hostname,user=username,password=passwd)
    dev.open()
    print "Login successful ..."
    ##print (dev.facts)
    
    ### Read application group data from SRX
    ### lab@srx2> show services application-identification statistics applications     
    apps = dev.rpc.get_appid_application_statistics()
    apps_groups = dev.rpc.get_appid_application_group_statistics()
    dev.close()
    print "Closing device ... "

    if database.report:
         print "Data already exist. Clearing old data."
         database.report.drop()

    if report.insert_entry(apps):
         print "Insert Successful!!"

# displays the initial form
@app.route('/', methods=['GET','POST'])
@app.route('/report',methods=['GET','POST'])
def present_get_input():
	if request.method == 'POST':
		hostname = request.form['hostname']
		username = request.form['user']
		passwd = request.form['password']

		read_device(hostname='172.27.62.23',username='lab',passwd='lab123')

		cursor = report.sort_by_kbytes()
		sort_by_kbytes = []
		for i in cursor:
		  #print i
		  sort_by_kbytes.append(i)
		return render_template('apptable.html',rows=sort_by_kbytes)
	return render_template("index.html")

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

@app.route("/build",methods=['GET','POST'])
def build():
  if request.method == 'POST':
    hostname = request.form['hostname']
    user = request.form['user']
    password = request.form['password']
    flash("INPUT SUBMITTED!")
    return render_template('build.html')
  return render_template('build.html')

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
    print RESULTS
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
        print "This app: ",i
        rows.append({
            "name" : i['name'],
            "sessions": i['sessions'],
            "bytes": i['bytes'],
            "category": i['category'],
            "is_encrypted": i['is_encrypted']
            })
    return render_template('http_apps.html',rows=rows)

if __name__ == '__main__':
	app.run(debug=True)

