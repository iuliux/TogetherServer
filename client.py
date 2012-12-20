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


A = ''
B = ''

# if resp['code'] != resp_ttoc['pad_already_exists']:
B_cr_n = -1
edit = ChangeRequest(author='B',
                    cr_n=B_cr_n,
                    pos=0,
                    delta=len(content),
                    op=ChangeRequest.ADD_EDIT,
                    value=content)
B_cr_n += 1

print 'Old B ::::::::::', B
conv = con_starter.new(method='PUT', resource=pad)
conv.send(edit.serialize())
print 'B commits "Hello, world!"'
print 'Code: ', conv.response_code
print 'Data: ', conv.response_data
if conv.response_code == 160:
    crs_to_update = EncodingHandler.deserialize_list(conv.response_data)
    for c in crs_to_update:
        c_cr = ChangeRequest()
        c_cr.deserialize(c)
        B = c_cr.apply_over(B)
    B_cr_n = int(conv.response_headers['new_cr_n'])
    print 'New CR_n: ', B_cr_n
else:
    B = edit.apply_over(B)
print 'New B ::::::::::', B
print
# else:
    # print 'ALREADY EXISTS'



A_cr_n = -1
edit = ChangeRequest(author='A',
                    cr_n=A_cr_n,
                    pos=0,
                    delta=len('Abba'),
                    op=ChangeRequest.ADD_EDIT,
                    value='Abba')
A_cr_n += 1

print 'Old A ::::::::::', A
conv = con_starter.new(method='PUT', resource=pad)
conv.send(edit.serialize())
print 'A commits "Abba"'
print 'Code: ', conv.response_code
print 'Data: ', conv.response_data
if conv.response_code == 160:
    crs_to_update = EncodingHandler.deserialize_list(conv.response_data)
    for c in crs_to_update:
        c_cr = ChangeRequest()
        c_cr.deserialize(c)
        A = c_cr.apply_over(A)
    A_cr_n = int(conv.response_headers['new_cr_n'])
    print 'New CR_n: ', A_cr_n
else:
    A = edit.apply_over(A)
print 'New A ::::::::::', A
print



edit = ChangeRequest(author='A',
                    cr_n=A_cr_n,
                    pos=0,
                    delta=1,
                    op=ChangeRequest.DEL_EDIT,
                    value='')
A_cr_n += 1

print 'Old A ::::::::::', A
conv = con_starter.new(method='PUT', resource=pad)
conv.send(edit.serialize())
print 'A commits "0-1"'
print 'Code: ', conv.response_code
print 'Data: ', conv.response_data
if conv.response_code == 160:
    crs_to_update = EncodingHandler.deserialize_list(conv.response_data)
    for c in crs_to_update:
        c_cr = ChangeRequest()
        c_cr.deserialize(c)
        A = c_cr.apply_over(A)
    A_cr_n = int(conv.response_headers['new_cr_n'])
    print 'New CR_n: ', A_cr_n
else:
    A = edit.apply_over(A)
print 'New A ::::::::::', A
print



edit = ChangeRequest(author='B',
                    cr_n=B_cr_n,
                    pos=0,
                    delta=len(content),
                    op=ChangeRequest.ADD_EDIT,
                    value=content)
B_cr_n += 1

print 'Old B ::::::::::', B
conv = con_starter.new(method='PUT', resource=pad)
conv.send(edit.serialize())
print 'B commits "Hello, world!" again'
print 'Code: ', conv.response_code
print 'Data: ', conv.response_data
if conv.response_code == 160:
    crs_to_update = EncodingHandler.deserialize_list(conv.response_data)
    for c in crs_to_update:
        c_cr = ChangeRequest()
        c_cr.deserialize(c)
        B = c_cr.apply_over(B)
    B_cr_n = int(conv.response_headers['new_cr_n'])
    print 'New CR_n: ', B_cr_n
else:
    B = edit.apply_over(B)
print 'New B ::::::::::', B
print




print 'Old A ::::::::::', A
conv = con_starter.new(method='GET', resource=pad)
conv.send(A_cr_n)
A_cr_n += 1
print 'A updates'
print 'Code: ', conv.response_code
print 'Data: ', conv.response_data
if conv.response_code == 160:
    crs_to_update = EncodingHandler.deserialize_list(conv.response_data)
    for c in crs_to_update:
        c_cr = ChangeRequest()
        c_cr.deserialize(c)
        A = c_cr.apply_over(A)
    A_cr_n = int(conv.response_headers['new_cr_n'])
    print 'New CR_n: ', A_cr_n
print 'New A ::::::::::', A
print




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
