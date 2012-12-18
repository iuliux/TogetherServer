# import httplib2

# http = httplib2.Http()
# response, content = http.request('http://localhost:8000/teebird')

# # print str(response)
# print str(content)

from communication import *

try:
    con_starter = ConversationStarter("http://localhost:8000")
except ConnectionError:
    pass

pad = 'newest_pad_in_town'
content = 'Hello, world!'

conv = con_starter.new(method='PUT', resource='')
conv.send(pad)
print conv.response_code
print conv.response_data

# if resp['code'] != resp_ttoc['pad_already_exists']:
edit = EncodingHandler.encode_edit(EncodingHandler.ADD_EDIT, 0, len(content), content)

conv = con_starter.new(method='PUT', resource=pad)
conv.send(edit)
print conv.response_data
# else:
    # print 'ALREADY EXISTS'

print 'Pad exists?'
conv = con_starter.new(method='GET', resource='')
conv.send(pad)
print conv.response_code

conv = con_starter.new(method='HEAD', resource=pad)
conv.send(pad)
print 'TIMESTAMP:', conv.response_data

conv = con_starter.new(method='HEAD', resource=pad+'/users')
conv.send(pad)
print 'NO. USERS:', conv.response_data
