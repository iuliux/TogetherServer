import time
from twisted.internet.protocol import Protocol
from changerequests import ChangeRequest, EncodingHandler

class TogetherProtocol(Protocol):

    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.factory.numProtocols = self.factory.numProtocols + 1
        self.transport.write(
            'Welcome! There are currently %d open connections.\n' %
            (self.factory.numProtocols,))

    def connectionLost(self, reason):
        self.factory.numProtocols = self.factory.numProtocols - 1

    def dataReceived(self, data):
        self.transport.write(data)




def time_millis():
    return int(time.time() * 1000)


class Pad(object):

    def __init__(self):
        self.last_mod = time_millis()
        # ChangeRequest (logic clock) number
        self.cr_n = -1
        # ChangeRequests list
        self.crs = []

        # Add it's personal Users resource
        self.users = Users()

    def is_update_needed(self, client_cr_n):
        return client_cr_n < self.cr_n

    def get_updates(self, client_cr_n):
        '''
        Get all updates
        Return serialized list of ChangeRequest changes
        '''
        ser_sendback = None
        if client_cr_n < self.cr_n:
            sendback = self.crs[client_cr_n+1:self.cr_n+1]
            enc_sendback = [i_cr.serialize() for i_cr in sendback]
            ser_sendback = EncodingHandler.serialize_list(enc_sendback)

        return ser_sendback

    def get_last_modif(self):
        ''' Get timestamp of the latest modification '''
        return self.last_mod

    def edit(self, encoded_edit):
        ''' Edit '''
        cr = ChangeRequest()
        cr.deserialize(encoded_edit)
        print "- EncCR: " + str(encoded_edit)
        print "- CurrCR: " + str(cr)

        self.last_mod = time_millis()
        self.cr_n += 1

        # Collect all CRs applied after the last update of author
        conflicts = self.crs[cr.cr_n+1:self.cr_n]

        if conflicts:
            # Update starting position for the new CR
            pos_delta = 0
            for confl in conflicts:
                if confl.pos < cr.pos:
                    pos_delta += confl.delta
            cr.pos += pos_delta

            # The list of CRs the client needs to apply to get up to date
            sendback = conflicts + [cr]
            enc_sendback = [i_cr.serialize() for i_cr in sendback]
            ser_sendback = EncodingHandler.serialize_list(enc_sendback)
        else:
            ser_sendback = ''

        # Add current CR to archive
        self.crs.append(cr)
        print "------ CRs: " + str(self.crs)

        return ser_sendback

    def unsubscribe_user(self, **params):
        ''' Discard user. Decrease reference count '''
        pass


class Users(object):
    # TODO

    def __init__(self):
        pass

    def GET(self, **params):
        ''' Get a list of all users '''
        return "GET"

    def HEAD(self, **params):
        ''' Get the _total_ number of users '''
        pass

    def PUT(self, **params):
        ''' Change the name of the requester '''
        pass


class PadsManager(object):
    def __init__(self):
        self.pads = {}

    def create_pad(self, pad_uri):
        ''' Create pad '''
        if pad_uri in self.pads:
            return 'pad_already_exists'
        else:
            self.pads[pad_uri] = Pad()
            return 'ok'

root = PadsManager()
