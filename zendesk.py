__author__ = 'Michael Yatsko'
#from zdesk import Zendesk
import base64
#zen = Zendesk("https://answers.callfire.com", "nocadmins@callfire.com", "C4llfire!")
#for ticket in zen.tickets_list():
#    print(ticket)
#    a = raw_input()
#    if a == '1':
#        break &&


from urllib import urlencode

import requests

credentials = base64.b64encode('nocadmins@callfire.com:C4llfire!')
session = requests.Session()
session.auth = credentials

params = {
    'query': 'type:ticket status:open',
    'sort_by': 'created_at',
    'sort_order': 'asc'
}

url = 'https://callfire.zendesk.com/api/v2/search.json?' + urlencode(params)
response = session.get(url)
if response.status_code != 200:
    print('Status:', response.status_code)
    exit()

data = response.json()
print(data)

#String encoded = Base64.encode((username + ":" + password).getBytes());
#??????request.addHeader("Authorization", "Basic " + encoded);
#Did you encoded and set it via Authorization header? - yes, urlencode does this