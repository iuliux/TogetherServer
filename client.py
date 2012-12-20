# import httplib2

# http = httplib2.Http()
# response, content = http.request('http://localhost:8000/teebird')

# # print str(response)
# print str(content)

from communication import *
from changerequests import *

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
edit = ChangeRequest(author='B',
                    cr_n=-1,
                    pos=0,
                    delta=len(content),
                    op=EncodingHandler.ADD_EDIT,
                    value=content)

conv = con_starter.new(method='PUT', resource=pad)
conv.send(edit.serialize())
print 'B commits "Hello, world!"'
print 'Code: ', conv.response_code
print 'Data: ', conv.response_data
# else:
    # print 'ALREADY EXISTS'

edit = ChangeRequest(author='A',
                    cr_n=-1,
                    pos=0,
                    delta=len('Abba'),
                    op=EncodingHandler.ADD_EDIT,
                    value='Abba')

conv = con_starter.new(method='PUT', resource=pad)
conv.send(edit.serialize())
print 'A commits "Abba"'
print 'Code: ', conv.response_code
print 'Data: ', conv.response_data
if conv.response_code == 160:
    new_cr_n = conv.response_headers['new_cr_n']
    print 'New CR_n: ', new_cr_n

edit = ChangeRequest(author='A',
                    cr_n=new_cr_n,
                    pos=0,
                    delta=1,
                    op=EncodingHandler.DEL_EDIT,
                    value='')

conv = con_starter.new(method='PUT', resource=pad)
conv.send(edit.serialize())
print 'A commits "0-1"'
print 'Code: ', conv.response_code
print 'Data: ', conv.response_data
if conv.response_code == 160:
    new_cr_n = conv.response_headers['new_cr_n']
    print 'New CR_n: ', new_cr_n


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
