__author__ = 'aleung'


#
# Copyright (c) 2008 - 2013 10gen, Inc. <http://10gen.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#

import sys
import re
import datetime


"""Normalize SRX app names
"""
def normalize(str):
   if len(str.split('_')) == 2:
       return '-'.join(str.split('_'))
   else:
       return str


# The Report Data Access Object handles interactions with the Reports collection
class ReportDAO:

    # constructor for the class
    def __init__(self, database):
        self.db = database
        # if collection_name already in database.collection_names(), drop it
        if database.report:
             print "Data already exist. Clearing old data."
             database.report.drop()
        self.report = database.report
        self.signatures = database.signatures

# else:
#      print "Data does not exist. Building new table..."

    ## Get the rest of the attribute from db.signatures collection

    # inserts the blog entry and returns a permalink for the entry
    def insert_entry(self, apps):
        last_reset_date = apps[0][0].text
        appgroup_list = apps.findall('appid-application-statistics/application-name')
        sessions_list = apps.findall('appid-application-statistics/sessions')
        kbyte_list = apps.findall('appid-application-statistics/bytes')
        is_encrypted_list = apps.findall('appid-application-statistics/is_encrypted')

        for app,session,byte,is_encrypted in zip(appgroup_list,sessions_list,kbyte_list,is_encrypted_list):
 
            each_app = normalize(app.text)

            cursor = self.signatures.find_one({"type":each_app})
            print "App: ", each_app
            print "Cursor: ",cursor
            risk = cursor['risk']
            category = cursor['category']
            subcategory = cursor['subcategory']
            ports = cursor['ports']
            characteristic = cursor['characteristic'] 

            entry = {"name": each_app,
                        "sessions": int(session.text),
                        "bytes": int(byte.text),
                         "category": category,
                         "subcategory": subcategory, 
                         "risk": int(risk),
                         "characteristic": characteristic,
                         "ports": ports,
                         "is_encrypted": is_encrypted.text
                        }

            # Now insert the post
            try:
                self.report.insert(entry)
                print "Inserting successful ..."
            except:
                print "Error inserting entry"
                print "Unexpected error:", sys.exc_info()[0]

        return True
    
    def sort_by_kbytes(self):
        return self.report.find({},{"_id":0,"name":1,"sessions":1,"bytes":1,"risk":1,"category":1,"subcategory":1,"is_encrypted":1}).sort("bytes",-1)

    def sort_by_sessions(self):
        return self.report.find({},{"_id":0,"name":1,"sessions":1,"bytes":1,"risk":1,"category":1,"subcategory":1,"is_encrypted":1}).sort("sessions",-1)

    def sort_by_apps(self):
        return self.report.find({},{"_id":0,"name":1,"sessions":1,"bytes":1,"risk":1,"category":1,"subcategory":1,"is_encrypted":1}).sort("name",1)

    def sort_by_risk(self):
        return self.report.find({},{"_id":0,"name":1,"sessions":1,"bytes":1,"risk":1,"category":1,"subcategory":1,"is_encrypted":1}).sort("risk",1)

    def sort_by_characteristic(self):
        character_dict = {'Known Vulnerabilities':0,'Can Leak Information':0,
              'Loss of Productivity':0,'Supports File Transfer':0,'Prone to Misuse':0,
              'Carrier of Malware':0,'Bandwidth Consumer':0,'Evasive':0,'Capable of Tunneling':0}
        
        cursor = self.report.aggregate([{"$unwind":"$characteristic"},
                {"$group":{"_id":"$characteristic","count":{"$sum":1}}}])
        return cursor

    def sort_by_subcategory(self):
        cursor = self.report.aggregate([{"$group":{"_id":"$subcategory",
              "app_count":{"$sum":1},"Sessions":{"$sum":"$sessions"},
              "Bytes":{"$sum":"$bytes"}}}])
        return cursor

    def sort_by_category(self):
        cursor = self.report.aggregate([{"$group":{"_id":"$category",
              "app_count":{"$sum":1},"Sessions":{"$sum":"$sessions"},
              "Bytes":{"$sum":"$bytes"}}}])
        return cursor
    
    def group_apps(self, limit):
        if limit > 0 :
            return (self.report.aggregate([
                {"$group":{"_id":"$name","count":{"$sum":"$bytes"}}},{"$sort":{"count":-1}},{"$limit": limit}])
                  )
        return (self.report.aggregate([
                {"$group":{"_id":"$name","count":{"$sum":"$bytes"}}},{"$sort":{"count":-1}}])
                  )

    def bubble_apps(self):
        cursor = self.report.aggregate([
                {"$group":{"_id":"$name","count":{"$sum":"$bytes"},"main_group":{"$addToSet":"$category"}}}])
        return cursor
        