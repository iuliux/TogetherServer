import cherrypy
import time

from server_helpers import *
from communication import *


def time_millis():
    return int(time.time() * 1000)


class Resource(object):
    """Template class for a resource"""
    def __init__(self):
        super(Resource, self).__init__()

    def set_response_code(self, rsp_type='generic_error'):
        cherrypy.response.headers['code'] = EncodingHandler.resp_ttoc[rsp_type]

    def set_response_header(self, hdr, data):
        cherrypy.response.headers[hdr] = data

    def get_request_body(self):
        return cherrypy.request.body.read()

    exposed = True

    def GET(self, **params):
        pass

    def HEAD(self, **params):
        pass

    def PUT(self, **params):
        pass

    def POST(self, **params):
        pass

    def DELETE(self, **params):
        pass


class Pad(Resource):

    def __init__(self):
        self.last_mod = time_millis()
        # ChangeRequest (logic clock) number
        self.cr_n = -1
        # ChangeRequests list
        self.crs = []

        # Add it's personal Users resource
        self.users = Users()

    """Get all updates"""
    def GET(self, **params):
        # cherrypy.log("SOMETHING")
        return str(params)

    """Get timestamp of the latest modification"""
    def HEAD(self, **params):
        self.set_response_header('data', str(self.last_mod))

    """Edit"""
    def PUT(self, **params):
        encoded_edit = self.get_request_body()
        cherrypy.log("EDIT: " + encoded_edit)

        self.last_mod = time_millis()

        self.set_response_code('ok')
        return encoded_edit

    """Discard user. Decrease reference count"""
    def DELETE(self, **params):
        pass


class Users(Resource):

    def __init__(self):
        pass

    """Get a list of all users"""
    def GET(self, **params):
        return "GET"

    """Get the _total_ number of users"""
    def HEAD(self, **params):
        pass

    """Change the name of the requester"""
    def PUT(self, **params):
        pass


class PadsManager(Resource):
    def __init__(self):
        super(Resource, self).__init__()

    """Check if pad exists"""
    def GET(self, **params):
        if hasattr(self, params['data']):
            self.set_response_code('yes')
        else:
            self.set_response_code('no')

    """?"""
    # def POST(self, **params):
    #     req = EncodingHandler.parse_msg(self.get_request_body())
    #     pass
    #     return req['code']

    """Create pad"""
    def PUT(self, **params):
        pad_uri = self.get_request_body()
        try:
            getattr(self, pad_uri)
            # Send appropriate error code
            self.set_response_code('pad_already_exists')
            return
        except AttributeError:
            setattr(self, pad_uri, Pad())
            self.set_response_code('ok')
            return

root = PadsManager()


cherrypy.quickstart(root, '/', 'server.conf')
