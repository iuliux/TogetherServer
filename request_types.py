import re

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


# Edit types
ADD_EDIT = 0
DEL_EDIT = 1


class EncodingHandler:

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
        if op_type == ADD_EDIT:
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

        op = DEL_EDIT
        if sections[2] == '+':
            op = ADD_EDIT

        edit_dict = {
            'cr_n': int(sections[0]),
            'pos': int(sections[1]),
            'op': op,
            'delta': int(sections[3]),
            'content': sections[4]
        }
        return edit_dict
