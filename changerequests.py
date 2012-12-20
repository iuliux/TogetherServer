"""Change-requests handling"""

from request_types import *


class ChangeRequest(object):
    """Class to represent and handle change requests"""

    def __init__(self, author='', cr_n=0, pos=0, delta=0, op=0, value=''):
        super(ChangeRequest, self).__init__()

        self.author, self.cr_n, self.pos, self.delta, self.op, self.value =\
            author, cr_n, pos, delta, op, value

    def serialize(self):
        """Produces a string that encodes the CR"""
        parts = {}
        parts['op'] = '-'
        if self.op == EncodingHandler.ADD_EDIT:
            parts['op'] = '+'
        # TODO: Encode numbers in a higher base (36)
        parts['auth'] = self.author
        parts['cr_n'] = str(self.cr_n)
        parts['pos'] = str(self.pos)
        parts['delta'] = str(self.delta)
        parts['content'] = self.value

        return "%(auth)s:%(cr_n)s:%(pos)s%(op)s%(delta)s:%(content)s:" % parts

    def deserialize(self, ser):
        pass

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        oper = 'n/a'
        if self.op == EncodingHandler.ADD_EDIT:
            oper = 'ins'
        elif self.op == EncodingHandler.DEL_EDIT:
            oper = 'del'

        if self.delta > 0:
            delta = '+' + str(self.delta)
        else:
            delta = str(self.delta)

        return '<' + self.author + '  CR:' + str(self.cr_n) +\
                '  (' + str(self.pos) + ':' + delta + ')  ' +\
                oper + ':' + str(self.value) + '>'
