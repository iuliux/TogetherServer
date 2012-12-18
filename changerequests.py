"""Change-requests handling"""

from request_types import *


class ChangeRequest(object):
    """Class to represent and handle change requests"""

    def __init__(self, author, cr_n, pos, delta, op, value):
        super(ChangeRequest, self).__init__()

        self.author, self.num, self.pos, self.delta, self.op, self.value =\
            author, cr_n, pos, delta, op, value

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
