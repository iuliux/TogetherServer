import re

resp_format = '%(code)d>%(args)s!'

# Request Type-to-Code
req_ttoc = {
    # PadsManager
        # GET  (10~19)
        'pad_exists':   10,

        # POST  (30~39)

        # PUT  (50~59)
        'new_pad':      50,

    # Resource(Pad)
        # GET  (20~29)
        'load':         20,
        'n_users':      21,
        'last_mod':     22,

        # POST  (40~49)
        'edit':         40,

        # PUT  (60~69)
}

# Response Type-to-Code
resp_ttoc = {
    'hello':    100,
    'ok':       101,
    'bad_code': 108,
    'bad_format': 109,

    # PadsManager
        # GET  (110~119)
        'yes':                  110,
        'no':                   111,

        # POST  (130~139)

        # PUT  (150~159)
        'pad_already_exists':   150,

    # Resource(Pad)
        # GET  (120~129)

        # POST  (140~149)

        # PUT  (160~169)
}

# For reverse looking up
req_ctot = {key: value for (value, key) in req_ttoc.items()}
resp_ctot = {key: value for (value, key) in resp_ttoc.items()}


class Parser:
    @staticmethod
    def parse_req(req):
        pattern = re.compile(r'(?P<req_type>[0-9]*?)\>(?P<value>.*?)!')
        try:
            sections = re.search(pattern, req).groups()
        except TypeError:
            return -1
        req_dict = {
            'code': int(sections[0]),
            'args': sections[1]
        }
        return req_dict

    @staticmethod
    def parse_resp(resp):
        print '>>>>>>>>', resp
        pattern = re.compile(r'(?P<req_type>[0-9]*?)\>(?P<value>.*?)!')
        try:
            sections = re.search(pattern, resp).groups()
        except TypeError:
            return -1
        ack = (int(sections[1]) == 1)
        return (sections[0], ack)

    # @staticmethod
    # def encode_edit(type, )
