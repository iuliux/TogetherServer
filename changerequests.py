"""Change-requests handling"""

from request_types import *


class ChangeRequest(object):
    """Class to represent and handle change requests"""

    def __init__(self, author, cr_n, pos, delta, op, value):
        super(ChangeRequest, self).__init__()

        self.author, self.num, self.pos, self.delta, self.op, self.value =\
            author, cr_n, pos, delta, op, value

    def serialize():
        """Produces a string that encodes the CR"""
        parts = {}
        parts['op'] = '-'
        if self.op == EncodingHandler.ADD_EDIT:
            parts['op'] = '+'
        # TODO: Encode numbers in a higher base (36)
        parts['cr_n'] = str(self.cr_n)
        parts['pos'] = str(self.pos)
        parts['delta'] = str(self.delta)
        parts['content'] = self.content

        return "%(cr_n)s:%(pos)s%(op)s%(delta)s:%(content)s:" % parts

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        oper = 'n/a'
        if self.op == ADD_EDIT:
            oper = 'ins'
        elif self.op == DEL_EDIT:
            oper = 'del'

        if self.delta > 0:
            delta = '+' + str(self.delta)
        else:
            delta = str(self.delta)

        return '<' + self.author.name + '  CR:' + str(self.author.cr_n) +\
                '  (' + str(self.pos) + ':' + delta + ')  ' +\
                oper + ':' + str(self.value) + '>'
