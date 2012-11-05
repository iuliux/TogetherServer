import cherrypy
import time

from request_types import *


def time_millis():
    return int(time.time() * 1000)


class Resource(object):

    def __init__(self, content):
        self.content = content
        self.last_mod = time_millis()
        self.cr_n = -1

    exposed = True

    """ Get details about pad """
    def GET(self, **params):
        cherrypy.log("SOMETHING")

        try:
            req_code = int(params['code'])
            if req_code == req_ttoc['load']:
                return self.content
            elif req_code == req_ttoc['last_mod']:
                return str(self.last_mod)

            # Send appropriate error code
            else:
                return EncodingHandler.assamble_resp('bad_code', req_code)
        except KeyError:
            return EncodingHandler.assamble_resp('bad_format')

        return str(params)

    """ Content management operations """
    def POST(self):
        req = EncodingHandler.parse_req(cherrypy.request.body.read())
        try:
            if req['code'] == req_ttoc['edit']:
                encoded_edit = req['args']

                self.last_mod = time_millis()

            # Send appropriate error code
            else:
                return EncodingHandler.assamble_resp('bad_code', req['code'])
        except KeyError:
            return EncodingHandler.assamble_resp('bad_format')

    """ ? """
    def PUT(self):
        pass


class PadsManager(Resource):
    def __init__(self):
        super(Resource, self).__init__()

    """ Get details about pads """
    def GET(self, **params):
        cherrypy.log("SOMETHING")

        try:
            req_code = int(params['code'])
            if req_code == req_ttoc['pad_exists']:
                if hasattr(self, params['args']):
                    return EncodingHandler.assamble_resp('yes', req_code)
                else:
                    return EncodingHandler.assamble_resp('no', req_code)

            # Send appropriate error code
            else:
                return EncodingHandler.assamble_resp('bad_code', req_code)
        except KeyError:
            return EncodingHandler.assamble_resp('bad_format')

        return str(params)

    """ ? """
    def POST(self):
        req = EncodingHandler.parse_req(cherrypy.request.body.read())
        pass
        return req['code']

    """ Create and destroy pads """
    def PUT(self):
        req = EncodingHandler.parse_req(cherrypy.request.body.read())
        try:
            if req['code'] == req_ttoc['new_pad']:
                pad_uri = req['args']
                try:
                    getattr(self, pad_uri)
                    return EncodingHandler.assamble_resp('pad_already_exists')
                except AttributeError:
                    setattr(self, pad_uri, Resource('NEW!'))
                    return EncodingHandler.assamble_resp('ok', req['code'])

            # Send appropriate error code
            else:
                return EncodingHandler.assamble_resp('bad_code', req['code'])
        except KeyError:
            return EncodingHandler.assamble_resp('bad_format', req_code)


root = PadsManager()


cherrypy.quickstart(root, '/', 'server.conf')
