import re

# Request Type-to-Code
req_ttoc = {
    # PadsManager
        # GET  (10~19)  :: Get details about pads
        'pad_exists':   10,  # Check if pad exists

        # POST  (30~39)  ::

        # PUT  (50~59)  :: Create and destroy pads
        'new_pad':      50,  # Instantiate a new pad

    # Resource(Pad)
        # GET  (20~29)  :: Get details about pad
        'load':         20,  # Get the whole content and CR-number of pad
        'n_users':      21,  # Get the number of current users
        'last_mod':     22,  # Timestamp of the latest edit

        # POST  (40~49)  :: Content management operations
        'edit':         40,  # Commit an edit

        # PUT  (60~69)  ::
}

# Response Type-to-Code
resp_ttoc = {
    'hello':        100,  #
    'ok':           101,  #
    'bad_code':     108,  #
    'bad_format':   109,  #

    # PadsManager
        # GET  (110~119)
        'yes':                  110,  #
        'no':                   111,  #

        # POST  (130~139)

        # PUT  (150~159)
        'pad_already_exists':   150,  #

    # Resource(Pad)
        # GET  (120~129)

        # POST  (140~149)

        # PUT  (160~169)
}

# For reverse looking up
req_ctot = {key: value for (value, key) in req_ttoc.items()}
resp_ctot = {key: value for (value, key) in resp_ttoc.items()}


# Edit types
ADD_EDIT = 0
DEL_EDIT = 1


class EncodingHandler:
    _encode_format = '%(code)d>%(args)s!'

    @staticmethod
    def parse_msg(msg):
        pattern = re.compile(r'(?P<msg_type>[0-9]+?)\>(?P<value>.*?)!')
        try:
            sections = re.search(pattern, msg).groups()
        except AttributeError:
            return None
        msg_dict = {
            'code': int(sections[0]),
            'args': sections[1]
        }
        return msg_dict

    @staticmethod
    def assamble_req(type_text, value=''):
        return EncodingHandler._assamble_msg(req_ttoc[type_text], value)

    @staticmethod
    def assamble_resp(type_text, value=''):
        return EncodingHandler._assamble_msg(resp_ttoc[type_text], value)

    @staticmethod
    def _assamble_msg(type_code, value):
        return EncodingHandler._encode_format % \
                {'code': type_code, 'args': str(value)}

    @staticmethod
    def encode_edit(type, position, delta, content):
        return ''
