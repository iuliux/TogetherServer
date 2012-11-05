import cherrypy
import time

from request_types import *


def time_millis():
    return int(time.time() * 1000)


class Resource(object):

    def __init__(self, content):
        self.content = content
        self.last_mod = time_millis()

    exposed = True

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
                return resp_format %\
                    {'code': resp_ttoc['bad_code'], 'args': str(req_code)}
        except KeyError:
            return resp_format %\
                {'code': resp_ttoc['bad_format'], 'args': str(req_code)}

        return str(params)

    def POST(self):
        req = Parser.parse_req(cherrypy.request.body.read())
        try:
            if req['code'] == req_ttoc['edit']:
                encoded_edit = req['args']

                self.last_mod = time_millis()

            # Send appropriate error code
            else:
                return resp_format %\
                    {'code': resp_ttoc['bad_code'], 'args': str(req['code'])}
        except KeyError:
            return resp_format %\
                {'code': resp_ttoc['bad_format'], 'args': str(req['code'])}

    def PUT(self):
        pass


class PadsManager(Resource):
    def __init__(self):
        super(Resource, self).__init__()

    def GET(self, **params):
        cherrypy.log("SOMETHING")

        try:
            req_code = int(params['code'])
            if req_code == req_ttoc['pad_exists']:
                if hasattr(self, params['args']):
                    return resp_format %\
                        {'code': resp_ttoc['yes'], 'args': str(req_code)}
                else:
                    return resp_format %\
                        {'code': resp_ttoc['no'], 'args': str(req_code)}

            # Send appropriate error code
            else:
                return resp_format %\
                    {'code': resp_ttoc['bad_code'], 'args': str(req_code)}
        except KeyError:
            return resp_format %\
                {'code': resp_ttoc['bad_format'], 'args': str(req_code)}

        return str(params)

    def POST(self):
        req = Parser.parse_req(cherrypy.request.body.read())
        pass
        return req['code']

    def PUT(self):
        req = Parser.parse_req(cherrypy.request.body.read())
        try:
            if req['code'] == req_ttoc['new_pad']:
                pad_uri = req['args']
                try:
                    getattr(self, pad_uri)
                    return resp_format %\
                        {'code': resp_ttoc['pad_already_exists'], 'args': ''}
                except AttributeError:
                    setattr(self, pad_uri, Resource('NEW!'))
                    return resp_format %\
                        {'code': resp_ttoc['ok'], 'args': str(req['code'])}

            # Send appropriate error code
            else:
                return resp_format %\
                    {'code': resp_ttoc['bad_code'], 'args': str(req['code'])}
        except KeyError:
            return resp_format %\
                {'code': resp_ttoc['bad_format'], 'args': str(req_code)}


root = PadsManager()


cherrypy.quickstart(root, '/', 'server.conf')
