import httplib
import base64
import string
import urllib
import time
import json

import mysql.connector

__author__ = 'myatsko'

# Getting data from RabbitMQ host
auth = 'Basic ' + string.strip(base64.encodestring('guest:guest'))
grab = httplib.HTTPConnection('mq-vip.prd.kernelfire.com:15672')
grab.putrequest("GET", "/api/queues")
grab.putheader('Authorization', auth)
grab.endheaders()
data = json.loads(grab.getresponse().read())

# Doing filtering and maths
res = float(0)
for i in data:
    if i["name"].startswith('text.outbound'):
        if "message_stats" in i:
            if "ack_details" in i["message_stats"]:
                res += float(i["message_stats"]["ack_details"]["rate"])

# Pushing to Statuspage.io
api_key = '338e353e-f119-4c1d-ade9-8e6f0b9df4ab'
page_id = 'nmm9j2skbrxf'
metric_id = 'yvdkckxxff5s'
api_base = 'api.statuspage.io'
ts = int(time.time())
params = urllib.urlencode({'data[timestamp]': ts, 'data[value]': res})
headers = {"Content-Type": "application/x-www-form-urlencoded", "Authorization": "OAuth " + api_key}
conn = httplib.HTTPSConnection(api_base)
conn.request("POST", "/v1/pages/" + page_id + "/metrics/" + metric_id + "/data.json", params, headers)
response = conn.getresponse()

# Pushing data to MySQL. dbtime commented out, because the db inserts time automatically
# dbtime = time.strftime('%c')
dbconn = mysql.connector.connect(user='myatsko', password='myfdbuqte4n', host='127.0.0.1', database='statuspage')
cursor = dbconn.cursor()
cursor.execute("""INSERT INTO message_rate (message_rate) VALUES (%s)""", (res,))
dbconn.commit()
cursor.close()
dbconn.close()
