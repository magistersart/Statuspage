import httplib
import urllib
import time
import json

import mysql.connector

__author__ = 'myatsko'

api_key = '338e353e-f119-4c1d-ade9-8e6f0b9df4ab'
page_id = 'nmm9j2skbrxf'
metric_id = 'ddkx7q7nrt59'
api_base = 'api.statuspage.io'
grab = httplib.HTTPConnection('192.168.6.73:8080')
grab.request("GET", "/callfire-delegator/activity-dashboard?format=json")
data = json.loads(grab.getresponse().read())
ts = int(time.time())
value = 0
for i in data["outbound-ccc-activity"]["accounts"]:
    if "agents" in i:
        value += i["agents"]
params = urllib.urlencode({'data[timestamp]': ts, 'data[value]': value})
headers = {"Content-Type": "application/x-www-form-urlencoded", "Authorization": "OAuth " + api_key}
conn = httplib.HTTPSConnection(api_base)
conn.request("POST", "/v1/pages/" + page_id + "/metrics/" + metric_id + "/data.json", params, headers)
response = conn.getresponse()

dbconn = mysql.connector.connect(user='myatsko', password='myfdbuqte4n', host='127.0.0.1', database='statuspage')
cursor = dbconn.cursor()
cursor.execute("""INSERT INTO active_agents (sum_active_agents) VALUES (%s)""", (value,))
dbconn.commit()
cursor.close()
dbconn.close()
