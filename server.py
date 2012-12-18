import cherrypy
import time

from server_helpers import *
from request_types import *


def time_millis():
    return int(time.time() * 1000)


class Resource(object):
    """Template class for a resource"""
    def __init__(self):
        super(Resource, self).__init__()

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
        cherrypy.response.headers['data']=str(self.last_mod)

    """Edit"""
    def PUT(self, **params):
        encoded_edit = cherrypy.request.body.read()
        cherrypy.log("EDIT: " + encoded_edit)

        self.last_mod = time_millis()

        cherrypy.response.headers['code'] = resp_ttoc['ok']
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
            cherrypy.response.headers['code'] = resp_ttoc['yes']
        else:
            cherrypy.response.headers['code'] = resp_ttoc['no']

    """?"""
    # def POST(self, **params):
    #     req = EncodingHandler.parse_msg(cherrypy.request.body.read())
    #     pass
    #     return req['code']

    """Create pad"""
    def PUT(self, **params):
        pad_uri = cherrypy.request.body.read()
        try:
            getattr(self, pad_uri)
            # Send appropriate error code
            cherrypy.response.headers['code'] = resp_ttoc['pad_already_exists']
            return
        except AttributeError:
            setattr(self, pad_uri, Pad())
            cherrypy.response.headers['code'] = resp_ttoc['ok']
            return

root = PadsManager()


cherrypy.quickstart(root, '/', 'server.conf')
