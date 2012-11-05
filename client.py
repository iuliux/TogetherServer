# import httplib2

# http = httplib2.Http()
# response, content = http.request('http://localhost:8000/teebird')

# # print str(response)
# print str(content)

from request_types import *

from restful_lib import Connection, ConnectionError

try:
    conn = Connection("http://localhost:8000")
except ConnectionError:
    pass

# print conn.request_get('teebird')[u'body']
# print str( conn.request_put(resource='teebird', body='<div>gg:12</div>')['headers']['status'] )

# print conn.request_post(resource='teebird', body=' ')['body']

body = str(req_ttoc["new_pad"]) + '>newest_pad_in_town!'

print conn.request_put(resource='', body=body)['body']

exists_check = {'code': req_ttoc["pad_exists"], 'args': 'newest_pad_in_town'}

print conn.request_get('', args=exists_check)['body']

get_code = {'code': req_ttoc['last_mod']}

print conn.request_get('newest_pad_in_town', args=get_code)['body']
