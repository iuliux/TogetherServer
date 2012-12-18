# Collaborative editing simulation


class ChangeRequest(object):
    INS = 1
    DEL = 2

    def __init__(self, author,  pos, delta, op, value):
        super(ChangeRequest, self).__init__()

        self.author, self.pos, self.delta, self.op, self.value =\
            author,  pos, delta, op, value

        self.num = self.author.cr_n
        self.author.next_cr_num()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        oper = 'n/a'
        if self.op == self.INS:
            oper = 'ins'
        elif self.op == self.DEL:
            oper = 'del'

        if self.delta > 0:
            delta = '+' + str(self.delta)
        else:
            delta = str(self.delta)

        return '<' + self.author.name + '  CR:' + str(self.author.cr_n) +\
                '  (' + str(self.pos) + ':' + delta + ')  ' +\
                oper + ':' + str(self.value) + '>'


class Server(object):
    def __init__(self):
        super(Server, self).__init__()

        self.cr_n = -1
        self.cr_list = []

    def commit(self, cr):
        self.cr_n += 1

        # TODO:
        # Daca vine un commit intarziat (s-au intamplat alte commituri de la
        # ultimul update al autorului prezent), autorul prezent trebuie obligat
        # sa aplice modificarile alea inainte sa o faca pe a lui.

        # Collect all CRs applied after the last update of cr.author
        conflicts = self.cr_list[cr.num+1:self.cr_n]

        [cr.author.apply(confl) for confl in conflicts]

        # Modifica CR-ul incat sa aiba noua pozitie (dupa eventuale modificari)

        # Update starting position for the new CR
        pos_delta = 0
        for confl in conflicts:
            if confl.pos < cr.pos:
                pos_delta += confl.delta
        cr.pos += pos_delta

        cr.author.apply(cr)
        cr.author.cr_n = self.cr_n

        # Add current CR to archive
        self.cr_list.append(cr)

    def update(self, client):
        for i in xrange(client.cr_n + 1, self.cr_n + 1):
            client.apply(self.cr_list[i])
        client.cr_n = self.cr_n


class Client(object):
    def __init__(self, name):
        super(Client, self).__init__()

        self.name = name
        self.cr_n = -1
        self.buffer = ''

    def next_cr_num(self):
        """Increments the CR number of self and also returns the new value"""
        self.cr_n += 1
        return self.cr_n

    def apply(self, cr):
        if cr.op == ChangeRequest.INS:
            head = self.buffer[:cr.pos]
            tail = self.buffer[cr.pos:]
            self.buffer = head + cr.value + tail
        elif cr.op == ChangeRequest.DEL:
            head = self.buffer[:cr.pos]
            tail = self.buffer[cr.pos+cr.value:]
            self.buffer = head + tail
        else:
            print 'UNKNOWN OPERATION'

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.name + '> ' + self.buffer + '  CR:' + str(self.cr_n)


s = Server()

a = Client('A')
b = Client('B')
c = Client('C')

# # Momentul 1
# s.commit(
#     ChangeRequest(a, 0, +5, ChangeRequest.INS, 'hello')
#     )
# print s.cr_list
# print 'BEFORE UPDATE'
# print a
# print b
# print c

# s.update(a)
# s.update(b)
# s.update(c)

# print 'AFTER UPDATE'
# print a
# print b
# print c

# # Momentul 2
# s.commit(
#     ChangeRequest(b, 0, -1, ChangeRequest.DEL, 1)
#     )
# s.commit(
#     ChangeRequest(b, 0, +1, ChangeRequest.INS, 'H')
#     )
# s.commit(
#     ChangeRequest(c, 5, +1, ChangeRequest.INS, '!')
#     )
# print s.cr_list
# print 'BEFORE UPDATE'
# print a
# print b
# print c

# s.update(a)
# s.update(b)
# s.update(c)

# print 'AFTER UPDATE'
# print a
# print b
# print c


# Momentul 1
s.commit(
    ChangeRequest(a, 0, +5, ChangeRequest.INS, 'hello')
    )
print s.cr_list
print 'BEFORE UPDATE'
print a
print b
print c

s.update(a)
s.update(b)
s.update(c)

print 'AFTER UPDATE'
print a
print b
print c

# Momentul 2
s.commit(
    ChangeRequest(b, 4, -1, ChangeRequest.DEL, 1)
    )
s.commit(
    ChangeRequest(b, 4, +3, ChangeRequest.INS, '!!!')
    )
s.commit(
    ChangeRequest(c, 0, -1, ChangeRequest.DEL, 1)
    )
s.commit(
    ChangeRequest(c, 0, +2, ChangeRequest.INS, '~H')
    )
s.commit(
    ChangeRequest(a, 4, +2, ChangeRequest.INS, ' n')
    )
print s.cr_list
print 'BEFORE UPDATE'
print a
print b
print c

s.update(a)
s.update(b)
s.update(c)

print 'AFTER UPDATE'
print a
print b
print c
