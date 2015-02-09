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



# The Report Data Access Object handles interactions with the Reports collection
class ReportDAO:

    # constructor for the class
    def __init__(self, database):
        self.db = database
        # if collection_name in database.collection_names():
        if database.report:
            print "Data already exist. Clearing old data."
            database.report.drop()
        self.report = database.report

# else:
#      print "Data does not exist. Building new table..."

    # inserts the blog entry and returns a permalink for the entry
    def insert_entry(self, apps):
        # print "inserting entry: ", app, sessions, bytes
        # print "Range: ", len(app)

        last_reset_date = apps[0][0].text
        appgroup_list = apps.findall('appid-application-statistics/application-name')
        sessions_list = apps.findall('appid-application-statistics/sessions')
        kbyte_list = apps.findall('appid-application-statistics/bytes')

        # app_groups = []    
        # app_sessions = []
        # bytes = []

        for app,session,byte in zip(appgroup_list,sessions_list,kbyte_list):
            #  app_groups.append(x.text)
            #  app_sessions.append(int(y.text))
            #  bytes.append(int(z.text)) 

            # #Build a new entry
            # for i in range(len(app)):
                entry = {"name": app.text,
                        "sessions": session.text,
                        "bytes": byte.text,
                        # "category":permalink,
                        # "subcategory": tags_array,
                        # "risk": risk,
                        # "characteristics": ch[],
                        # "ports": ports[]
                        }

                # # now insert the post
                try:
                    self.report.insert(entry)
                    print "Inserting the entry"
                except:
                    print "Error inserting entry"
                    print "Unexpected error:", sys.exc_info()[0]

        return True



