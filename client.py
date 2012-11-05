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



req = EncodingHandler.assamble_req('new_pad', 'newest_pad_in_town')
encresp = conn.request_put(resource='', body=req)['body']
resp = EncodingHandler.parse_msg(encresp)

if resp['code'] != resp_ttoc['pad_already_exists']:
    pass

exists_check = {'code': req_ttoc["pad_exists"], 'args': 'newest_pad_in_town'}

print conn.request_get(resource='', args=exists_check)['body']

get_code = {'code': req_ttoc['last_mod']}

print conn.request_get(resource='newest_pad_in_town', args=get_code)['body']
