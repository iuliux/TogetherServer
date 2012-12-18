import re
from restful_lib import Connection


class ConversationStarter:
    """Factory class for Conversation objects"""

    def __init__(self, target_uri):
        self.uri = target_uri
        self.conn = Connection(target_uri)

    def new(self, method, resource=''):
        return Conversation(self.conn, method, resource)


class Conversation:
    """
    A conversation is a sequence of one request followed by one response.
    To be produced from a ConversationStarter factory.
    """

    def __init__(self, conn, method, resource):
        self._conn = conn
        self._method = method.upper()
        self._resource = resource
        self.response_code = 0
        self.response_data = ''
        self.response_headers = {}

    def send(self, data='', headers={}):
        """
        Sends the request and receives the response
        After this method finishes, response data will be available
        """
        if self._method == 'GET':
            resp = self._conn.request_get(resource=self._resource,
                                            args={'data': data},
                                            headers=headers)
        elif self._method == 'DELETE':
            resp = self._conn.request_delete(resource=self._resource,
                                            body=data,
                                            headers=headers)
        elif self._method == 'HEAD':
            resp = self._conn.request_head(resource=self._resource,
                                            headers=headers)
        elif self._method == 'POST':
            resp = self._conn.request_post(resource=self._resource,
                                            body=data,
                                            headers=headers)
        elif self._method == 'PUT':
            resp = self._conn.request_put(resource=self._resource,
                                            body=data,
                                            headers=headers)
        # else raise UndefinedMethodError

        # Set response data
        self.response_headers = resp['headers']

        if self._method == 'HEAD':
            try:
                self.response_data = resp['headers']['data']
            except KeyError:
                pass
        else:
            self.response_data = resp['body']

        try:
            self.response_code = int(resp['headers']['code'])
        except KeyError:
            pass


class UndefinedMethodError(Exception):
    def __str__(self):
        return "Undefined HTTP method. Try on of: GET, POST, PUT, HEAD, DELETE"


class EncodingHandler:
    # Edit types
    ADD_EDIT = 0
    DEL_EDIT = 1

    # Response Type-to-Code
    resp_ttoc = {
        'ok':               101,  # Generic success message
        'generic_error':    108,  # Generic fail message

        # PadsManager
            # GET  (110~119)
            'yes':                  110,  # Positive answer
            'no':                   111,  # Negative answer (not error)

            # POST  (130~139)

            # PUT  (150~159)
            'pad_already_exists':   '150',  # Error message

        # Resource(Pad)
            # GET  (120~129)

            # POST  (140~149)

            # PUT  (160~169)
    }
    # For reverse look-up
    resp_ctot = {key: value for (value, key) in resp_ttoc.items()}

    @staticmethod
    def encode_edit(cr_n, op_type, pos, delta, content=''):
        """Encodes an edit command. Arguments:
            cr_n - (logic clock) number of this change-request
            op_type - edit operation (+ / -)
            pos - position of the edit
            delta - number of modified characters
            content - actual edit data (needed only for additions)
        """
        op = '-'
        if op_type == EncodingHandler.ADD_EDIT:
            op = '+'

        # TODO: Encode numbers in a higher base (36)
        return str(cr_n) + ':' + str(pos) + op + str(delta) + \
                ':' + content + ':'

    @staticmethod
    def decode_edit(edit):
        """Decodes an encoded edit. Returns a dict:
            cr_n - (logic clock) number of this change-request
            pos - position of the edit
            op - edit operation (+ / -)
            delta - number of modified characters
            content - actual edit data (empty for deletions)
        """
        pattern = re.compile(
            r'(?P<cr>[0-9]+?):(?P<pos>[0-9]+?)(?P<op>[+-]?)(?P<delta>[0-9]+?):(?P<data>.*?):'
        )
        try:
            sections = re.search(pattern, edit).groups()
        except AttributeError:
            return None

        op = EncodingHandler.DEL_EDIT
        if sections[2] == '+':
            op = EncodingHandler.ADD_EDIT

        edit_dict = {
            'cr_n': int(sections[0]),
            'pos': int(sections[1]),
            'op': op,
            'delta': int(sections[3]),
            'content': sections[4]
        }
        return edit_dict
